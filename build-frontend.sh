#!/bin/bash

# Build script for CEZ HDO frontend card

set -e

FRONTEND_DIR="custom_components/cez_hdo/frontend"
DIST_DIR="$FRONTEND_DIR/dist"

echo "🏗️  Building CEZ HDO frontend card..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ to build the frontend."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm to build the frontend."
    exit 1
fi

# Navigate to frontend directory
cd "$FRONTEND_DIR"

echo "📦 Installing dependencies..."
npm install

echo "🔨 Building production bundle..."
npm run build

echo "✅ Frontend build completed successfully!"

# Check if build output exists
if [ -f "$DIST_DIR/cez-hdo-card.js" ]; then
    echo "📄 Built file: $(du -h $DIST_DIR/cez-hdo-card.js | cut -f1) cez-hdo-card.js"
else
    echo "❌ Build failed - no output file found"
    exit 1
fi

echo ""
echo "🎉 CEZ HDO frontend card is ready!"
echo ""
echo "To use the card:"
echo "1. Restart Home Assistant"
echo "2. Add the card to your Lovelace dashboard:"
echo "   type: custom:cez-hdo-card"
echo ""
