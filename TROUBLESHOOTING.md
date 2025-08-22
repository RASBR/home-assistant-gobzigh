# GOBZIGH Integration - Image Display Troubleshooting

## Issue Fixed: Static File Serving

The main issue was that the integration was missing the static file serving setup. This has been fixed by:

1. **Added static path registration** in `__init__.py`:
   ```python
   hass.http.register_static_path(
       f"/api/{DOMAIN}/static",
       static_path,
       cache_headers=False
   )
   ```

2. **Updated Home Assistant minimum version** to `2024.1.0` to ensure compatibility with the static path registration method.

3. **Added debug logging** to help identify static path registration issues.

## Changes Made

### Files Modified:
- `custom_components/gobzigh/__init__.py` - Added static path registration
- `custom_components/gobzigh/manifest.json` - Updated minimum HA version
- `test_static_files.py` - Created test script (NEW FILE)

### Key Improvements:
1. **Proper Static File Serving**: Images are now served via Home Assistant's HTTP server
2. **Modern API Usage**: Using current `register_static_path` method instead of deprecated approaches
3. **Debug Logging**: Added logging to track static path registration
4. **Version Compatibility**: Updated to require HA 2024.1.0+

## How to Test the Fix

### Step 1: Restart Home Assistant
After making these changes, restart Home Assistant completely (not just reload the integration).

### Step 2: Check Logs
Look for this log message in Home Assistant logs:
```
Registered static path: /api/gobzigh/static -> [path_to_integration]/static
```

### Step 3: Test Static Files
Run the test script:
```bash
python3 test_static_files.py
```

### Step 4: Verify in UI
- Go to Developer Tools → States
- Find a sensor like `sensor.your_tank_fill_percentage`
- Check if it has an `entity_picture` attribute
- The entity should show custom liquid level images

## What Images Are Used

### Liquid Level Icons (Dynamic):
- `water_0.png` to `water_5.png` - Water level indicators (0-100%)
- `diesel_0.png` to `diesel_5.png` - Diesel/oil level indicators (0-100%)

### Device Icons:
- `gobzigh-1.png` - WLSV0 device model
- `gobzigh-2.png` - Other device models

### Brand Icons:
- `icon.png` / `dark_icon.png` - Integration icons
- `logo.png` / `dark_logo.png` - Brand logos

## Expected Behavior After Fix

1. **Fill Percentage Sensors** should show dynamic liquid level images based on percentage:
   - 0-5%: level_0.png (nearly empty)
   - 5-20%: level_1.png (low)
   - 20-40%: level_2.png (medium-low)
   - 40-60%: level_3.png (medium)
   - 60-80%: level_4.png (medium-high)
   - 80-100%: level_5.png (full)

2. **Image URLs** should be accessible at:
   ```
   http://your-ha-ip:8123/api/gobzigh/static/water_0.png
   http://your-ha-ip:8123/api/gobzigh/static/diesel_3.png
   etc.
   ```

3. **Entity Cards** in the UI should display the appropriate liquid level images.

## Troubleshooting

### If Images Still Don't Show:

1. **Check Browser Cache**: Hard refresh (Ctrl+F5) or open in incognito mode
2. **Check File Permissions**: Ensure static files are readable
3. **Check Integration Logs**: Look for any error messages related to static path registration
4. **Verify File Paths**: Ensure all image files exist in the `static/` directory
5. **Test Direct URLs**: Try accessing image URLs directly in browser

### Common Issues:
- **Permission Denied**: Check file system permissions on static directory
- **404 Not Found**: Static path registration failed - check logs
- **Images Not Updating**: Browser cache issue - clear cache or hard refresh

## Developer Notes

The integration now uses:
- **`entity_picture`** property for custom images (correct approach)
- **`icon`** property for Material Design Icons (fallback)
- **Modern static file serving** compatible with Home Assistant 2024.1+
- **Proper error handling** and logging for troubleshooting

No deprecated methods are used in the current implementation.
