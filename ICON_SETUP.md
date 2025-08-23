# GOBZIGH Integration Icon Setup

## Problem Solved

The GOBZIGH integration icon was not showing in Home Assistant due to several issues:

1. **Path Mismatch**: The manifest.json was referencing `static/gobzigh/icon.png` but the HTTP handler could only serve files from the root static directory.

2. **Missing Files**: Some referenced icon files were missing from the expected locations.

3. **HTTP Handler Limitations**: The original HTTP handler used `Path(filename).name` which stripped directory paths, preventing subdirectory access.

## Solutions Implemented

### 1. Fixed HTTP Handler (`http.py`)
- Enhanced path handling to support subdirectories safely
- Added proper path traversal protection
- Improved logging for debugging icon serving issues
- Better error handling and fallback mechanisms

### 2. Icon File Structure
Created comprehensive icon structure:

```
custom_components/gobzigh/
├── icon.png                    # Main integration icon (for Home Assistant UI)
├── icon.svg                    # Vector version (preferred by Home Assistant)
├── logo.svg                    # Logo version
├── static/
│   ├── icon.png               # Served via HTTP API
│   ├── icon@2x.png           # High-res version
│   ├── logo.png              # Logo for branding
│   ├── dark_icon.png         # Dark theme support
│   ├── dark_logo.png         # Dark theme logo
│   ├── gobzigh-1.png         # Device-specific icons
│   ├── gobzigh-2.png
│   └── gobzigh/              # Original subfolder (kept for compatibility)
│       ├── icon.png
│       └── icon@2x.png
```

### 3. Updated manifest.json
- Set icon path to `icon.png` (relative to integration root)
- This follows Home Assistant's standard convention

## Icon Serving URLs

The integration now serves icons via these URLs:
- `/api/gobzigh/static/icon.png` - Main icon
- `/api/gobzigh/static/logo.png` - Logo
- `/api/gobzigh/static/dark_icon.png` - Dark theme icon
- `/api/gobzigh/static/gobzigh-1.png` - Device model icons
- `/api/gobzigh/static/water_0.png` through `water_5.png` - Level indicators
- `/api/gobzigh/static/diesel_0.png` through `diesel_5.png` - Fuel level indicators

## Testing

To test if the icons are working:

1. **Integration Icon**: Check the Home Assistant integrations page
2. **HTTP Endpoints**: Visit `http://your-ha-instance:8123/api/gobzigh/static/icon.png`
3. **Entity Icons**: Look at the GOBZIGH entities in the UI
4. **Logs**: Check Home Assistant logs for any "GOBZIGH static file server" messages

## Fallback Strategy

Home Assistant will now look for icons in this order:
1. brands repository (online) - not available for custom integrations
2. Local integration folder (`icon.png`, `icon.svg`)
3. HTTP API static files (`/api/gobzigh/static/...`)
4. Default MDI icons as final fallback

This ensures maximum compatibility and fallback coverage.
