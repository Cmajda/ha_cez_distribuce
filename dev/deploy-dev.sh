#!/bin/bash

# ČEZ HDO Development Deploy Script
# Builds frontend and deploys to local dev Home Assistant
#
# Usage:
#   ./deploy-dev.sh                          # Deploy to default /mnt/ha-config
#   ./deploy-dev.sh clean                    # Remove integration from HA
#   HA_CONFIG_DIR=/path/to/ha ./deploy-dev.sh # Custom HA config path
#
# Environment variables:
#   HA_CONFIG_DIR - Path to Home Assistant configuration directory
#                   Default: /mnt/ha-config

set -e

# Configuration
# Auto-detect project directory (parent of dev folder)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Target directories - customize these for your Home Assistant installation
TARGET_DIR="${HA_CONFIG_DIR:-/mnt/ha-config}/custom_components/cez_hdo"
WWW_TARGET="${HA_CONFIG_DIR:-/mnt/ha-config}/www/cez_hdo"

set -e

# Check for clean parameter
if [ "$1" = "clean" ]; then
    echo "🧹 ČEZ HDO Development Cleanup"
    echo "=============================="

    # Configuration
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
    TARGET_DIR="${HA_CONFIG_DIR:-/mnt/ha-config}/custom_components/cez_hdo"
    WWW_TARGET="${HA_CONFIG_DIR:-/mnt/ha-config}/www/cez_hdo"

    # Colors
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    NC='\033[0m'

    echo "🎯 Target directory: $TARGET_DIR"
    echo "🌐 WWW directory: $WWW_TARGET"
    echo ""

    # Remove component
    if [ -d "$TARGET_DIR" ]; then
        echo -e "${YELLOW}🗑️  Removing ČEZ HDO component...${NC}"
        rm -rf "$TARGET_DIR"
        echo -e "${GREEN}✅ Component removed from $TARGET_DIR${NC}"
    else
        echo -e "${YELLOW}⚠️  Component not found in $TARGET_DIR${NC}"
    fi

    # Remove frontend from www
    if [ -f "$WWW_TARGET/cez-hdo-card.js" ]; then
        echo -e "${YELLOW}🗑️  Removing frontend card...${NC}"
        rm -f "$WWW_TARGET/cez-hdo-card.js"
        echo -e "${GREEN}✅ Frontend card removed from $WWW_TARGET${NC}"
    else
        echo -e "${YELLOW}⚠️  Frontend card not found in $WWW_TARGET${NC}"
    fi

    # Clean Python cache
    echo -e "${YELLOW}🧹 Cleaning Python cache...${NC}"
    find "${HA_CONFIG_DIR:-/mnt/ha-config}/custom_components" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find "${HA_CONFIG_DIR:-/mnt/ha-config}/custom_components" -name "*.pyc" -delete 2>/dev/null || true
    echo -e "${GREEN}✅ Python cache cleaned${NC}"

    # Ask about configuration removal
    CONFIG_FILE="${HA_CONFIG_DIR:-/mnt/ha-config}/configuration.yaml"
    if [ -f "$CONFIG_FILE" ] && grep -q "platform: cez_hdo" "$CONFIG_FILE"; then
        echo ""
        echo -e "${YELLOW}❓ Remove ČEZ HDO configuration from configuration.yaml? [y/N]${NC}"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            # Backup before removing
            cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"

            # Remove ČEZ HDO configuration (from comment to end of binary_sensor block)
            sed -i '/# ČEZ HDO integrace/,/^binary_sensor:/{ /^binary_sensor:/!d; }' "$CONFIG_FILE"
            sed -i '/^binary_sensor:/,/platform: cez_hdo/{ /platform: cez_hdo/,/scan_interval: 300/d; }' "$CONFIG_FILE"

            echo -e "${GREEN}✅ ČEZ HDO configuration removed from configuration.yaml${NC}"
            echo -e "${YELLOW}📝 Backup saved with timestamp${NC}"
        else
            echo -e "${YELLOW}⚠️  Configuration left in configuration.yaml (manual removal needed)${NC}"
        fi
    fi

    echo ""
    echo -e "${GREEN}✨ ČEZ HDO cleanup completed!${NC}"
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "   1. Restart Home Assistant"
    echo "   2. Check that entities are gone"
    echo "   3. Verify Lovelace card is removed"
    echo "   4. Check configuration.yaml if needed"
    echo ""

    exit 0
fi

echo "🚀 ČEZ HDO Development Deployment"
echo "=================================="
echo "📁 Project directory: $PROJECT_DIR"
echo "🎯 Target directory: $TARGET_DIR"
echo "🌐 WWW directory: $WWW_TARGET"
echo ""

# You can override HA_CONFIG_DIR by setting environment variable:
# export HA_CONFIG_DIR="/path/to/your/homeassistant/config"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Step 1: Version checking
echo -e "${BLUE}🔍 Step 1: Checking versions...${NC}"
DEV_VERSION=$(grep '"version"' "$PROJECT_DIR/dev/cez_hdo/manifest.json" | sed 's/.*"version": "\([^"]*\)".*/\1/')
PROD_VERSION=$(grep '"version"' "$PROJECT_DIR/custom_components/cez_hdo/manifest.json" | sed 's/.*"version": "\([^"]*\)".*/\1/' 2>/dev/null || echo "none")

echo "📦 Dev version: $DEV_VERSION"
echo "🏠 Production version: $PROD_VERSION"

if [ "$DEV_VERSION" != "$PROD_VERSION" ]; then
    echo -e "${YELLOW}⚠️  Version mismatch detected, will update production${NC}"
fi

# Step 2: Build frontend
echo -e "${BLUE}📦 Step 2: Building frontend...${NC}"
cd "$PROJECT_DIR/dev/frontend"

if command -v npm >/dev/null 2>&1; then
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing npm dependencies..."
        npm install
    fi

    # Build frontend
    echo "Building production bundle..."
    npm run build
    echo -e "${GREEN}✅ Frontend build completed${NC}"
else
    echo -e "${YELLOW}⚠️  npm not found, skipping frontend build${NC}"
fi

# Step 3: Clean existing installation
echo -e "${BLUE}🧹 Step 3: Cleaning existing installation...${NC}"
rm -rf "$TARGET_DIR"
find /mnt/ha-config/custom_components -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find /mnt/ha-config/custom_components -name "*.pyc" -delete 2>/dev/null || true

# Create necessary directories
mkdir -p "$(dirname "$TARGET_DIR")"
mkdir -p "$WWW_TARGET"
echo -e "${GREEN}✅ Cleanup completed${NC}"

# Step 4: Deploy component files
echo -e "${BLUE}📁 Step 4: Deploying component files...${NC}"
mkdir -p "$TARGET_DIR/frontend/dist"

# Copy Python files from dev
    cp "$PROJECT_DIR/dev/cez_hdo"/*.py "$TARGET_DIR/"
    cp "$PROJECT_DIR/dev/cez_hdo/manifest.json" "$TARGET_DIR/"

# Copy built frontend files
if [ -f "$PROJECT_DIR/dev/frontend/dist/cez-hdo-card.js" ]; then
    cp "$PROJECT_DIR/dev/frontend/dist"/* "$TARGET_DIR/frontend/dist/"
    echo -e "${GREEN}✅ Frontend files copied from dev build${NC}"
else
    echo -e "${YELLOW}⚠️  Dev frontend build not found, checking production...${NC}"
    # Fallback to production files
    if [ -f "$PROJECT_DIR/custom_components/cez_hdo/frontend/dist/cez-hdo-card.js" ]; then
        cp "$PROJECT_DIR/custom_components/cez_hdo/frontend/dist"/* "$TARGET_DIR/frontend/dist/"
        echo -e "${YELLOW}⚠️  Using production frontend files${NC}"
    fi
fi

echo -e "${GREEN}✅ Component files deployed${NC}"

# Step 5: HACS Frontend Integration
echo -e "${BLUE}🌐 Step 5: HACS Frontend Integration...${NC}"
echo -e "${GREEN}✅ Frontend will be served automatically by HACS from:${NC}"
echo -e "${GREEN}   /hacsfiles/integrations/cez_hdo/cez-hdo-card.js${NC}"
echo -e "${YELLOW}ℹ️  No manual www deployment needed - HACS handles frontend${NC}"

# Step 6: Verification
echo -e "${BLUE}🔍 Step 6: Verification...${NC}"
if [ -d "$TARGET_DIR" ] && [ -f "$TARGET_DIR/__init__.py" ]; then
    echo -e "${GREEN}✅ Component installed successfully${NC}"

    echo "📂 Files installed:"
    ls -la "$TARGET_DIR" | head -10

    if [ -f "$WWW_TARGET/cez-hdo-card.js" ]; then
        echo -e "\n🌐 Frontend file:"
        ls -la "$WWW_TARGET/cez-hdo-card.js"
    fi
else
    echo -e "${RED}❌ Installation failed!${NC}"
    exit 1
fi

# Step 7: Configuration setup
echo -e "${BLUE}⚙️ Step 7: Checking configuration...${NC}"
CONFIG_FILE="${HA_CONFIG_DIR:-/mnt/ha-config}/configuration.yaml"

if [ -f "$CONFIG_FILE" ]; then
    # Check if ČEZ HDO configuration already exists
    if grep -q "platform: cez_hdo" "$CONFIG_FILE"; then
        echo -e "${YELLOW}⚠️  ČEZ HDO configuration already exists in configuration.yaml${NC}"
    else
        echo -e "${BLUE}📝 Adding ČEZ HDO configuration to configuration.yaml...${NC}"

        # Backup configuration file
        cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${GREEN}✅ Configuration backup created${NC}"

        # Add configuration
        cat >> "$CONFIG_FILE" << 'EOF'

# ČEZ HDO integrace
sensor:
  - platform: cez_hdo
    code: "405"  # Váš distribuční kód
    region: stred # Váš region
    scan_interval: 300  # Aktualizace každých 5 minut (volitelné)

binary_sensor:
  - platform: cez_hdo
    code: "405"  # Váš distribuční kód
    region: stred # Váš region
    scan_interval: 300  # Aktualizace každých 5 minut (volitelné)
EOF

        echo -e "${GREEN}✅ ČEZ HDO configuration added to configuration.yaml${NC}"
        echo -e "${YELLOW}📝 Note: Update code and region parameters as needed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  configuration.yaml not found at $CONFIG_FILE${NC}"
fi

echo ""
echo -e "${GREEN}✨ ČEZ HDO deployment completed!${NC}"
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "   1. Update code and region in configuration.yaml if needed"
echo "   2. Restart Home Assistant"
echo "   3. Check logs for any errors"
echo "   4. Verify entities are working"
echo "   5. Test Lovelace card functionality"
