#!/bin/bash

# CEZ HDO Component Reinstallation Script
# Completely removes and reinstalls the component with cache cleanup

echo "🔄 Starting CEZ HDO component reinstallation..."

# Change to project directory
cd /home/cmajda/Projects/Doma/ha_cez_distribuce

echo "🗑️  Step 1: Removing existing component..."
# Remove existing component completely
sudo rm -rf /mnt/ha-config/custom_components/cez_hdo
echo "   ✅ Component removed"

echo "🧹 Step 2: Cleaning Python cache..."
# Clean Python cache from entire custom_components directory
sudo find /mnt/ha-config/custom_components -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
sudo find /mnt/ha-config/custom_components -name "*.pyc" -delete 2>/dev/null || true
echo "   ✅ Python cache cleaned"

echo "📁 Step 3: Creating fresh directory structure..."
# Create fresh directory structure
sudo mkdir -p /mnt/ha-config/custom_components/cez_hdo
sudo mkdir -p /mnt/ha-config/custom_components/cez_hdo/frontend/dist
echo "   ✅ Directory structure created"

echo "📦 Step 4: Installing Python files..."
# Copy Python files
sudo cp custom_components/cez_hdo/__init__.py /mnt/ha-config/custom_components/cez_hdo/
sudo cp custom_components/cez_hdo/base_entity.py /mnt/ha-config/custom_components/cez_hdo/
sudo cp custom_components/cez_hdo/binary_sensor.py /mnt/ha-config/custom_components/cez_hdo/
sudo cp custom_components/cez_hdo/downloader.py /mnt/ha-config/custom_components/cez_hdo/
sudo cp custom_components/cez_hdo/sensor.py /mnt/ha-config/custom_components/cez_hdo/
sudo cp custom_components/cez_hdo/manifest.json /mnt/ha-config/custom_components/cez_hdo/
echo "   ✅ Python files installed"

echo "🎨 Step 5: Installing frontend files..."
# Copy frontend files
sudo cp custom_components/cez_hdo/frontend/dist/* /mnt/ha-config/custom_components/cez_hdo/frontend/dist/ 2>/dev/null || true
# Also copy to www for Lovelace
sudo mkdir -p /mnt/ha-config/www
sudo cp custom_components/cez_hdo/frontend/dist/cez-hdo-card.js /mnt/ha-config/www/ 2>/dev/null || true
echo "   ✅ Frontend files installed"

echo "🔍 Step 6: Verification..."
# Verify installation
if [ -f "/mnt/ha-config/custom_components/cez_hdo/__init__.py" ]; then
    echo "   ✅ Component installed successfully"
    echo "   📂 Files installed:"
    ls -la /mnt/ha-config/custom_components/cez_hdo/
    echo ""
    echo "   🎨 Frontend files:"
    ls -la /mnt/ha-config/custom_components/cez_hdo/frontend/dist/ 2>/dev/null || echo "   ⚠️  No frontend files found"
    echo ""
    echo "   🌐 WWW files:"
    ls -la /mnt/ha-config/www/cez-hdo-card.js 2>/dev/null || echo "   ⚠️  No WWW card file found"
else
    echo "   ❌ Installation failed!"
    exit 1
fi

echo ""
echo "✨ CEZ HDO component reinstallation completed!"
echo "📋 Next steps:"
echo "   1. Restart Home Assistant"
echo "   2. Check logs for any errors"
echo "   3. Verify entities are working"
echo "   4. Test Lovelace card functionality"
echo ""