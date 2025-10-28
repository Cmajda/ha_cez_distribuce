#!/bin/bash

# CEZ HDO Card Build Script
set -e

echo "🔨 Building CEZ HDO Card..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Navigate to www directory
cd "$(dirname "$0")/www"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Type checking
echo "🔍 Running type check..."
npm run type-check

# Linting
echo "🧹 Running linter..."
npm run lint

# Build the card
echo "🏗️  Building production bundle..."
npm run build

echo "✅ Build completed successfully!"
echo "📁 Output files are in www/dist/"

# Copy to main directory for easy access
if [ -f "dist/cez-hdo-card.js" ]; then
    cp dist/cez-hdo-card.js ../cez-hdo-card.js
    echo "📋 Copied cez-hdo-card.js to main directory"
fi

echo "🎉 CEZ HDO Card is ready to use!"
