#!/usr/bin/env python3
"""
GOBZIGH Integration Installation Script

This script helps install the GOBZIGH integration to your Home Assistant instance.
"""

import os
import shutil
import sys
from pathlib import Path


def find_ha_config_dir():
    """Find Home Assistant configuration directory."""
    # Common Home Assistant config paths
    possible_paths = [
        Path.home() / ".homeassistant",
        Path("/config"),  # Docker/Supervisor
        Path.home() / "homeassistant",
        Path("/usr/share/hassio/homeassistant"),
    ]
    
    for path in possible_paths:
        if path.exists() and (path / "configuration.yaml").exists():
            return path
    
    return None


def main():
    """Main installation function."""
    print("GOBZIGH Home Assistant Integration Installer")
    print("=" * 50)
    
    # Find source directory (where this script is)
    script_dir = Path(__file__).parent
    source_dir = script_dir / "custom_components" / "gobzigh"
    
    if not source_dir.exists():
        print(f"❌ Error: Source directory not found at {source_dir}")
        print("Make sure you're running this script from the integration directory.")
        sys.exit(1)
    
    # Find Home Assistant config directory
    ha_config_dir = find_ha_config_dir()
    if not ha_config_dir:
        print("❌ Could not automatically find Home Assistant configuration directory.")
        ha_config_input = input("Please enter the path to your Home Assistant config directory: ")
        ha_config_dir = Path(ha_config_input)
        
        if not ha_config_dir.exists():
            print(f"❌ Error: Directory {ha_config_dir} does not exist.")
            sys.exit(1)
    
    print(f"✅ Found Home Assistant config directory: {ha_config_dir}")
    
    # Create custom_components directory if it doesn't exist
    custom_components_dir = ha_config_dir / "custom_components"
    custom_components_dir.mkdir(exist_ok=True)
    
    # Target directory for the integration
    target_dir = custom_components_dir / "gobzigh"
    
    # Check if integration already exists
    if target_dir.exists():
        overwrite = input(f"⚠️  Integration already exists at {target_dir}. Overwrite? (y/N): ")
        if overwrite.lower() != 'y':
            print("Installation cancelled.")
            sys.exit(0)
        
        # Remove existing installation
        shutil.rmtree(target_dir)
        print("🗑️  Removed existing installation")
    
    # Copy integration files
    try:
        shutil.copytree(source_dir, target_dir)
        print(f"✅ Successfully installed GOBZIGH integration to {target_dir}")
    except Exception as e:
        print(f"❌ Error copying files: {e}")
        sys.exit(1)
    
    # Verify installation
    required_files = [
        "manifest.json",
        "__init__.py", 
        "config_flow.py",
        "const.py",
        "sensor.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not (target_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️  Warning: Missing files: {', '.join(missing_files)}")
    else:
        print("✅ All required files installed successfully")
    
    print("\n📋 Next Steps:")
    print("1. Restart Home Assistant")
    print("2. Go to Configuration → Integrations")
    print("3. Click 'Add Integration' and search for 'GOBZIGH'")
    print("4. Enter your GOBZIGH User ID when prompted")
    print("5. Your devices will be automatically discovered!")
    
    print(f"\n📁 Integration installed at: {target_dir}")
    print("🔧 Check the README.md file in the integration directory for detailed usage instructions.")


if __name__ == "__main__":
    main()
