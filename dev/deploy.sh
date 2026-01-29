#!/bin/bash

# ČEZ HDO Development Deploy Script

# Show help if requested
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "ČEZ HDO Development Deploy Script"
    echo "Builds frontend and deploys to local dev Home Assistant"
    echo "#----------------------------------------------------------#"
    echo "Usage:"
    echo "  ./deploy.sh [EAN] [IP] [PASSWORD]              -- Deploy with parameters"
    echo "  ./deploy.sh                                    -- Deploy using environment variables"
    echo "  ./deploy.sh clean [IP] [PASSWORD]              -- Remove integration from HA"
    echo "#----------------------------------------------------------#"
    echo "Environment variables (used if parameters not provided):"
    echo "  EAN           - EAN number (18 digits)"
    echo "  HA_IP         - IP address of Home Assistant"
    echo "  HA_PASSWORD   - Password for CIFS mount"
    echo "  HA_USERNAME   - Username for CIFS mount (default: current user)"
    echo "  HA_CONFIG_DIR - Path to Home Assistant configuration directory"
    echo "                  Default: /mnt/ha-config"
    echo "#----------------------------------------------------------#"
    echo "Examples:"
    echo "  EAN=123458786461864646 HA_IP=192.168.1.1 HA_PASSWORD=pass ./deploy.sh"
    echo "  ./deploy.sh 123458786461864646 192.168.1.1 mypassword"
    echo "  ./deploy.sh clean 192.168.1.1 mypassword"
    exit 0
fi

set -e

# Configuration
# Auto-detect project directory (parent of dev folder)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Parse command line arguments
CLEAN_MODE=""

# Check if first argument is "clean"
if [ "$1" = "clean" ]; then
    CLEAN_MODE="clean"
    # For clean mode: clean [IP] [PASSWORD]
    HA_IP="${2:-$HA_IP}"
    HA_PASSWORD="${3:-$HA_PASSWORD}"
else
    # For deploy mode: [EAN] [IP] [PASSWORD]
    # Parameters override environment variables
    if [ -n "$1" ]; then
        EAN="$1"
    fi
    if [ -n "$2" ]; then
        HA_IP="$2"
    fi
    if [ -n "$3" ]; then
        HA_PASSWORD="$3"
    fi
fi

# Validate required variables for deploy mode
if [ "$CLEAN_MODE" != "clean" ] && [ -z "$EAN" ]; then
    echo "❌ EAN not provided. Set EAN environment variable or pass as first argument."
    echo "   Example: EAN=123458786461864646 ./deploy.sh"
    echo "   Example: ./deploy.sh 123458786461864646"
    exit 1
fi

# Default mount point
MOUNT_POINT="${HA_CONFIG_DIR:-/mnt/ha-config}"

# Target directories
TARGET_DIR="$MOUNT_POINT/custom_components/cez_hdo"

# Source directory (this repo)
SRC_DIR="$PROJECT_DIR/custom_components/cez_hdo"

# Function to setup CIFS mount
setup_mount() {
    local ha_ip="$1"
    local ha_password="$2"
    local username="${HA_USERNAME:-$USER}"

    if [ -z "$ha_ip" ]; then
        echo "⚠️  No HA IP provided, assuming mount already exists"
        return 0
    fi

    echo "🔗 Setting up CIFS mount to $ha_ip..."

    # Check if mount point exists and is mounted
    if mountpoint -q "$MOUNT_POINT" 2>/dev/null; then
        echo "✅ Mount already active at $MOUNT_POINT"
        return 0
    fi

    # Create mount point if it doesn't exist
    if [ ! -d "$MOUNT_POINT" ]; then
        echo "📁 Creating mount point: $MOUNT_POINT"
        sudo mkdir -p "$MOUNT_POINT"
    fi

    # Unmount if something is there but not working
    sudo umount "$MOUNT_POINT" 2>/dev/null || true

    # Mount with password or prompt for it
    if [ -n "$ha_password" ]; then
        echo "🔑 Mounting with provided password..."
        echo "$ha_password" | sudo mount -t cifs "//$ha_ip/config" "$MOUNT_POINT" \
            -o username="$username",vers=3.0,uid=$(id -u),gid=$(id -g),iocharset=utf8,file_mode=0777,dir_mode=0777,password-stdin
    else
        echo "🔑 Please enter password for $username@$ha_ip:"
        sudo mount -t cifs "//$ha_ip/config" "$MOUNT_POINT" \
            -o username="$username",vers=3.0,uid=$(id -u),gid=$(id -g),iocharset=utf8,file_mode=0777,dir_mode=0777
    fi

    # Verify mount
    if mountpoint -q "$MOUNT_POINT" && [ -f "$MOUNT_POINT/configuration.yaml" ]; then
        echo "✅ Mount successful - Home Assistant config detected"
        return 0
    else
        echo "❌ Mount failed or Home Assistant config not found"
        return 1
    fi
}

set -e

# Check for clean parameter
if [ "$CLEAN_MODE" = "clean" ]; then
    echo "🧹 ČEZ HDO Development Cleanup"
    echo "=============================="

    # Setup mount if needed
    if ! mountpoint -q "$MOUNT_POINT" 2>/dev/null; then
        if ! setup_mount "$HA_IP" "$HA_PASSWORD"; then
            echo "❌ Failed to setup mount for cleanup"
            exit 1
        fi
    fi

    # Configuration
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
    TARGET_DIR="$MOUNT_POINT/custom_components/cez_hdo"

    # Colors
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    NC='\033[0m'

    echo "🎯 Target directory: $TARGET_DIR"
    echo ""

    # Remove component
    if [ -d "$TARGET_DIR" ]; then
        echo -e "${YELLOW}🗑️  Removing ČEZ HDO component...${NC}"
        rm -rf "$TARGET_DIR"
        echo -e "${GREEN}✅ Component removed from $TARGET_DIR${NC}"
    else
        echo -e "${YELLOW}⚠️  Component not found in $TARGET_DIR${NC}"
    fi

    # Clean Python cache
    echo -e "${YELLOW}🧹 Cleaning Python cache...${NC}"
    find "$MOUNT_POINT/custom_components" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$MOUNT_POINT/custom_components" -name "*.pyc" -delete 2>/dev/null || true
    echo -e "${GREEN}✅ Python cache cleaned${NC}"

    # Ask about configuration removal
    CONFIG_FILE="$MOUNT_POINT/configuration.yaml"
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

# Setup mount if needed
if ! mountpoint -q "$MOUNT_POINT" 2>/dev/null; then
    if ! setup_mount "$HA_IP" "$HA_PASSWORD"; then
        echo "❌ Failed to setup mount. Please check IP address and credentials."
        exit 1
    fi
fi

echo "📁 Project directory: $PROJECT_DIR"
echo "🎯 Target directory: $TARGET_DIR"
echo "🧩 Card URL: /cez_hdo_card/cez-hdo-card.js"
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
SRC_VERSION=$(grep '"version"' "$SRC_DIR/manifest.json" | sed 's/.*"version": "\([^"]*\)".*/\1/' 2>/dev/null || echo "unknown")
INSTALLED_VERSION=$(grep '"version"' "$TARGET_DIR/manifest.json" | sed 's/.*"version": "\([^"]*\)".*/\1/' 2>/dev/null || echo "none")

echo "📦 Source version: $SRC_VERSION"
echo "🏠 Installed version: $INSTALLED_VERSION"

if [ "$SRC_VERSION" != "$INSTALLED_VERSION" ]; then
    echo -e "${YELLOW}⚠️  Version differs, will deploy update${NC}"
fi

# Step 2: Build frontend
echo -e "${BLUE}📦 Step 2: Building frontend...${NC}"
FRONTEND_DEV_DIR="$PROJECT_DIR/dev/frontend"
FRONTEND_COMPONENT_DIR="$SRC_DIR/frontend/dist"

if [ -d "$FRONTEND_DEV_DIR" ]; then
    cd "$FRONTEND_DEV_DIR"

    if command -v npm >/dev/null 2>&1; then
        # Install dependencies if needed
        if [ ! -d "node_modules" ]; then
            echo "Installing npm dependencies..."
            npm install
        fi

        # Build frontend (production = no console.log)
        echo "Building production bundle (console.log removed)..."
        npm run build:prod
        echo -e "${GREEN}✅ Frontend build completed${NC}"

        # Copy built files to component source directory
        if [ -f "$FRONTEND_DEV_DIR/dist/cez-hdo-card.js" ]; then
            mkdir -p "$FRONTEND_COMPONENT_DIR"
            cp "$FRONTEND_DEV_DIR/dist"/* "$FRONTEND_COMPONENT_DIR/"
            echo -e "${GREEN}✅ Frontend copied to component source: $FRONTEND_COMPONENT_DIR${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  npm not found, skipping frontend build${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  dev/frontend not found, skipping frontend build${NC}"
fi

# Step 3: Clean existing installation
echo -e "${BLUE}🧹 Step 3: Cleaning existing installation...${NC}"
rm -rf "$TARGET_DIR"
find "$MOUNT_POINT/custom_components" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$MOUNT_POINT/custom_components" -name "*.pyc" -delete 2>/dev/null || true

# Create necessary directories
mkdir -p "$(dirname "$TARGET_DIR")"
echo -e "${GREEN}✅ Cleanup completed${NC}"

# Step 4: Deploy component files
echo -e "${BLUE}📁 Step 4: Deploying component files...${NC}"
if [ ! -d "$SRC_DIR" ]; then
    echo -e "${RED}❌ Source directory not found: $SRC_DIR${NC}"
    exit 1
fi

mkdir -p "$TARGET_DIR"

# Copy full integration from custom_components/cez_hdo
cp -a "$SRC_DIR/." "$TARGET_DIR/"

echo -e "${GREEN}✅ Component deployed (includes built frontend)${NC}"

# Step 5: Verification
echo -e "${BLUE}🔍 Step 6: Verification...${NC}"
if [ -d "$TARGET_DIR" ] && [ -f "$TARGET_DIR/__init__.py" ]; then
    echo -e "${GREEN}✅ Component installed successfully${NC}"

    echo "📂 Files installed:"
    ls -la "$TARGET_DIR" | head -10
else
    echo -e "${RED}❌ Installation failed!${NC}"
    exit 1
fi

# Step 6: Configuration setup
echo -e "${BLUE}⚙️ Step 6: Checking configuration...${NC}"
CONFIG_FILE="$MOUNT_POINT/configuration.yaml"

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
        if [ -n "$EAN" ]; then
            cat >> "$CONFIG_FILE" << EOF

# ČEZ HDO integrace
sensor:
  - platform: cez_hdo
    ean: "$EAN"

binary_sensor:
  - platform: cez_hdo
    ean: "$EAN"
EOF
        else
            echo -e "${RED}❌ EAN not set. Set EAN environment variable or add to variables_local.ini${NC}"
            exit 1
        fi

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
