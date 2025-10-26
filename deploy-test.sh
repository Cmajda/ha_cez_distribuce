#!/bin/bash

# CEZ HDO Test Deploy Script
set -e

echo "🔌 CEZ HDO Test Deployment Script"
echo "=================================="

# Konfigurace
HA_IP="192.168.1.233"
HA_SHARE="config"
MOUNT_POINT="/mnt/ha-config"
PROJECT_DIR="/home/cmajda/Projects/Doma/ha_cez_distribuce"

# Barvy pro output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📡 Connecting to Home Assistant...${NC}"

# Vytvoř mount point pokud neexistuje
if [ ! -d "$MOUNT_POINT" ]; then
    echo "Creating mount point..."
    sudo mkdir -p "$MOUNT_POINT"
fi

# Připoj síťovou cestu (zkus různé možnosti)
echo "Mounting network share..."
if sudo mount -t cifs "//$HA_IP/$HA_SHARE" "$MOUNT_POINT" -o guest,uid=$(id -u),gid=$(id -g) 2>/dev/null; then
    echo -e "${GREEN}✅ Mounted successfully with guest access${NC}"
elif sudo mount -t cifs "//$HA_IP/$HA_SHARE" "$MOUNT_POINT" -o guest,vers=1.0,uid=$(id -u),gid=$(id -g) 2>/dev/null; then
    echo -e "${GREEN}✅ Mounted successfully with SMB v1.0${NC}"
else
    echo -e "${RED}❌ Failed to mount. Please check network and permissions.${NC}"
    echo "Try manual mount:"
    echo "sudo mount -t cifs //$HA_IP/$HA_SHARE $MOUNT_POINT -o username=YOUR_USER,password=YOUR_PASS,uid=\$(id -u),gid=\$(id -g)"
    exit 1
fi

# Ověř připojení
if [ ! -d "$MOUNT_POINT/custom_components" ]; then
    echo -e "${YELLOW}⚠️  custom_components directory not found, creating...${NC}"
    sudo mkdir -p "$MOUNT_POINT/custom_components"
fi

echo -e "${YELLOW}📦 Deploying CEZ HDO component...${NC}"

# Smaž starou verzi pokud existuje
if [ -d "$MOUNT_POINT/custom_components/cez_hdo" ]; then
    echo "Removing old version..."
    sudo rm -rf "$MOUNT_POINT/custom_components/cez_hdo"
fi

# Zkopíruj novou verzi
echo "Copying new version..."
cd "$PROJECT_DIR"
sudo cp -r custom_components/cez_hdo "$MOUNT_POINT/custom_components/"

# Ověř kopírování
if [ -f "$MOUNT_POINT/custom_components/cez_hdo/manifest.json" ]; then
    echo -e "${GREEN}✅ Component copied successfully${NC}"
    echo "Files deployed:"
    ls -la "$MOUNT_POINT/custom_components/cez_hdo/"
else
    echo -e "${RED}❌ Copy failed${NC}"
    exit 1
fi

# Zkontroluj frontend soubory
if [ -f "$MOUNT_POINT/custom_components/cez_hdo/frontend/dist/cez-hdo-card.js" ]; then
    echo -e "${GREEN}✅ Frontend files found${NC}"
    CARD_SIZE=$(du -h "$MOUNT_POINT/custom_components/cez_hdo/frontend/dist/cez-hdo-card.js" | cut -f1)
    echo "Custom card size: $CARD_SIZE"
else
    echo -e "${YELLOW}⚠️  Frontend files not found - custom card won't work${NC}"
fi

echo -e "${YELLOW}🔄 Restarting Home Assistant...${NC}"

# Restart HA (zkus různé způsoby)
echo "Attempting HA restart..."

# Metoda 1: REST API (potřebuje token)
if [ ! -z "$HA_TOKEN" ]; then
    if curl -s -X POST \
        -H "Authorization: Bearer $HA_TOKEN" \
        -H "Content-Type: application/json" \
        "http://$HA_IP:8123/api/services/homeassistant/restart" > /dev/null; then
        echo -e "${GREEN}✅ HA restart initiated via API${NC}"
    fi
else
    echo -e "${YELLOW}💡 Set HA_TOKEN environment variable for automatic restart${NC}"
    echo "export HA_TOKEN='your_long_lived_access_token'"
fi

# Umount
echo "Unmounting..."
sudo umount "$MOUNT_POINT" 2>/dev/null || true

echo -e "${GREEN}🎉 Deployment completed!${NC}"
echo ""
echo "Next steps:"
echo "1. Wait for HA to restart (~30 seconds)"
echo "2. Check Developer Tools → States for new entities:"
echo "   - binary_sensor.cez_hdo_lowtariffactive"
echo "   - binary_sensor.cez_hdo_hightariffactive"
echo "   - sensor.cez_hdo_* (6 sensors)"
echo "3. Add custom card to dashboard:"
echo "   type: custom:cez-hdo-card"
echo "4. Check browser console for card loading"
echo ""
echo -e "${YELLOW}📚 Configuration needed in configuration.yaml:${NC}"
echo "binary_sensor:"
echo "  - platform: cez_hdo"
echo "    region: stred  # your region"
echo "    code: 405     # your code"
echo ""
echo "sensor:"
echo "  - platform: cez_hdo"
echo "    region: stred"
echo "    code: 405"