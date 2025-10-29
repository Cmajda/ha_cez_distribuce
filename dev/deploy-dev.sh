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
WWW_TARGET="${HA_CONFIG_DIR:-/mnt/ha-config}/www"

set -e

# Check for clean parameter
if [ "$1" = "clean" ]; then
    echo "🧹 ČEZ HDO Development Cleanup"
    echo "=============================="
    
    # Configuration
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
    TARGET_DIR="${HA_CONFIG_DIR:-/mnt/ha-config}/custom_components/cez_hdo"
    WWW_TARGET="${HA_CONFIG_DIR:-/mnt/ha-config}/www"
    
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
    
    echo ""
    echo -e "${GREEN}✨ ČEZ HDO cleanup completed!${NC}"
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "   1. Restart Home Assistant"
    echo "   2. Check that entities are gone"
    echo "   3. Verify Lovelace card is removed"
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
DEV_VERSION=$(grep '"version"' "$PROJECT_DIR/dev/src/manifest.json" | sed 's/.*"version": "\([^"]*\)".*/\1/')
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
cp "$PROJECT_DIR/dev/src"/*.py "$TARGET_DIR/"
cp "$PROJECT_DIR/dev/src/manifest.json" "$TARGET_DIR/"

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

# Step 5: Deploy frontend to www
echo -e "${BLUE}🌐 Step 5: Deploying frontend to www...${NC}"
# Create www directory if it doesn't exist
mkdir -p "$WWW_TARGET"

if [ -f "$TARGET_DIR/frontend/dist/cez-hdo-card.js" ]; then
    cp "$TARGET_DIR/frontend/dist/cez-hdo-card.js" "$WWW_TARGET/"
    echo -e "${GREEN}✅ Frontend deployed to www${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend file not found${NC}"
fi

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

echo ""
echo -e "${GREEN}✨ ČEZ HDO deployment completed!${NC}"
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "   1. Restart Home Assistant"
echo "   2. Check logs for any errors"
echo "   3. Verify entities are working"
echo "   4. Test Lovelace card functionality"