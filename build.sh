#!/bin/bash

# CEZ HDO Build Script
# Automaticky builduje frontend a kopíruje soubory na správná místa

set -e

echo "🔨 Building CEZ HDO Frontend..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$SCRIPT_DIR/custom_components/cez_hdo/frontend"

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo -e "${RED}❌ Frontend directory not found: $FRONTEND_DIR${NC}"
    exit 1
fi

cd "$FRONTEND_DIR"

echo -e "${BLUE}📁 Working in: $FRONTEND_DIR${NC}"

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ package.json not found. Run npm init first.${NC}"
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    npm install
fi

# Run build
echo -e "${YELLOW}🔨 Building TypeScript...${NC}"
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful!${NC}"
    
    # Show output files
    if [ -d "dist" ]; then
        echo -e "${BLUE}📄 Generated files:${NC}"
        ls -la dist/
        
        # Calculate file sizes
        for file in dist/*; do
            if [ -f "$file" ]; then
                size=$(du -h "$file" | cut -f1)
                echo -e "${GREEN}  📄 $(basename "$file"): $size${NC}"
            fi
        done
    fi
    
    echo -e "${GREEN}🎉 CEZ HDO Frontend build completed successfully!${NC}"
    echo -e "${BLUE}💡 Files are ready in: $FRONTEND_DIR/dist${NC}"
else
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

# Optional: Run development server
read -p "🚀 Do you want to start development server? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🚀 Starting development server...${NC}"
    npm run dev
fi