#!/usr/bin/env python3
"""
Validation script for Gobzigh Home Assistant Integration
This script checks if all required files are present and properly structured.
"""

import json
import os
from pathlib import Path

def main():
    """Main validation function."""
    print("🔍 Gobzigh Integration Validator")
    print("===============================")
    print()
    
    # Check if we're in the right directory
    integration_dir = Path("custom_components/gobzigh")
    if not integration_dir.exists():
        print("❌ Error: custom_components/gobzigh directory not found")
        print("   Make sure you're running this from the repository root")
        return False
    
    success = True
    
    # Required files
    required_files = [
        "custom_components/gobzigh/__init__.py",
        "custom_components/gobzigh/manifest.json",
        "custom_components/gobzigh/config_flow.py",
        "custom_components/gobzigh/coordinator.py",
        "custom_components/gobzigh/sensor.py",
        "custom_components/gobzigh/switch.py",
        "custom_components/gobzigh/const.py",
        "custom_components/gobzigh/strings.json",
        "custom_components/gobzigh/icon.png",
        "custom_components/gobzigh/logo.png",
        "custom_components/gobzigh/translations/en.json",
    ]
    
    print("📋 Checking required files...")
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - MISSING")
            success = False
    
    print()
    
    # Validate manifest.json
    print("📄 Validating manifest.json...")
    try:
        with open("custom_components/gobzigh/manifest.json") as f:
            manifest = json.load(f)
        
        required_keys = ["domain", "name", "config_flow", "requirements", "version"]
        for key in required_keys:
            if key in manifest:
                print(f"   ✅ {key}: {manifest[key]}")
            else:
                print(f"   ❌ {key} - MISSING")
                success = False
                
        # Check domain matches directory
        if manifest.get("domain") != "gobzigh":
            print(f"   ❌ domain mismatch: expected 'gobzigh', got '{manifest.get('domain')}'")
            success = False
            
    except Exception as e:
        print(f"   ❌ Error reading manifest.json: {e}")
        success = False
    
    print()
    
    # Check image files
    print("🖼️  Checking image files...")
    for img_file in ["icon.png", "logo.png"]:
        img_path = Path(f"custom_components/gobzigh/{img_file}")
        if img_path.exists():
            size = img_path.stat().st_size
            print(f"   ✅ {img_file} ({size} bytes)")
        else:
            print(f"   ❌ {img_file} - MISSING")
            success = False
    
    print()
    
    # Validate translations
    print("🌐 Validating translations...")
    try:
        with open("custom_components/gobzigh/translations/en.json") as f:
            translations = json.load(f)
        
        if "config" in translations:
            print("   ✅ Config translations found")
        else:
            print("   ❌ Config translations missing")
            success = False
            
    except Exception as e:
        print(f"   ❌ Error reading translations: {e}")
        success = False
    
    print()
    
    # Final result
    if success:
        print("🎉 All validations passed!")
        print("   Your Gobzigh integration is ready for installation!")
    else:
        print("❌ Some validations failed.")
        print("   Please fix the issues above before installation.")
    
    return success

if __name__ == "__main__":
    main()
