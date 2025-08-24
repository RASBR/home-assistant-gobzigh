#!/bin/bash

# Gobzigh Integration Installation Script for Home Assistant
# This script helps install the Gobzigh integration into your Home Assistant instance

set -e

echo "🏠 Gobzigh Home Assistant Integration Installer"
echo "=============================================="
echo ""

# Check if Home Assistant config directory exists
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_home_assistant_config>"
    echo "Example: $0 /config"
    echo "         $0 ~/.homeassistant"
    exit 1
fi

CONFIG_DIR="$1"
CUSTOM_COMPONENTS_DIR="$CONFIG_DIR/custom_components"
GOBZIGH_DIR="$CUSTOM_COMPONENTS_DIR/gobzigh"

echo "📁 Installing to: $CONFIG_DIR"
echo ""

# Create custom_components directory if it doesn't exist
if [ ! -d "$CUSTOM_COMPONENTS_DIR" ]; then
    echo "📂 Creating custom_components directory..."
    mkdir -p "$CUSTOM_COMPONENTS_DIR"
fi

# Check if gobzigh integration already exists
if [ -d "$GOBZIGH_DIR" ]; then
    echo "⚠️  Gobzigh integration already exists at $GOBZIGH_DIR"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Installation cancelled."
        exit 1
    fi
    echo "🗑️  Removing existing installation..."
    rm -rf "$GOBZIGH_DIR"
fi

# Copy the integration
echo "📋 Copying Gobzigh integration files..."
cp -r "custom_components/gobzigh" "$CUSTOM_COMPONENTS_DIR/"

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Restart Home Assistant"
echo "2. Go to Configuration → Integrations"
echo "3. Click '+ ADD INTEGRATION'"
echo "4. Search for 'Gobzigh' and select it"
echo "5. Enter your 24-character User ID"
echo "6. Add discovered devices as needed"
echo ""
echo "📖 For more information, see:"
echo "   - README.md for detailed documentation"
echo "   - CONFIGURATION.md for setup guide"
echo ""
echo "🎉 Enjoy your new Gobzigh integration!"
