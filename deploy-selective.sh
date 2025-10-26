#!/bin/bash

# CEZ HDO Selective Deploy Script
set -e

echo "🚀 Deploying ČEZ HDO - Production files only"

PROJECT_DIR="/home/cmajda/Projects/Doma/ha_cez_distribuce"
TARGET_DIR="/mnt/ha-config/custom_components/cez_hdo"

# Smaž starou verzi
if [ -d "$TARGET_DIR" ]; then
    echo "Removing old version..."
    sudo rm -rf "$TARGET_DIR"
fi

# Vytvoř strukturu
echo "Creating directory structure..."
sudo mkdir -p "$TARGET_DIR/frontend/dist"

# Kopíruj Python soubory
echo "Copying Python files..."
cd "$PROJECT_DIR"
sudo cp custom_components/cez_hdo/__init__.py "$TARGET_DIR/"
sudo cp custom_components/cez_hdo/manifest.json "$TARGET_DIR/"
sudo cp custom_components/cez_hdo/base_entity.py "$TARGET_DIR/"
sudo cp custom_components/cez_hdo/binary_sensor.py "$TARGET_DIR/"
sudo cp custom_components/cez_hdo/sensor.py "$TARGET_DIR/"
sudo cp custom_components/cez_hdo/downloader.py "$TARGET_DIR/"

# Kopíruj pouze built frontend
echo "Copying frontend files..."
if [ -f "custom_components/cez_hdo/frontend/dist/cez-hdo-card.js" ]; then
    sudo cp custom_components/cez_hdo/frontend/dist/* "$TARGET_DIR/frontend/dist/"
    echo "✅ Frontend files copied"
else
    echo "⚠️  Frontend files not found - run ./build.sh first"
fi

# Nastavit práva
sudo chown -R cmajda:cmajda "$TARGET_DIR" 2>/dev/null || true

echo "✅ Deployment completed!"
echo ""
echo "Files deployed:"
find "$TARGET_DIR" -type f | sort
echo ""
echo "Total size:"
du -sh "$TARGET_DIR"