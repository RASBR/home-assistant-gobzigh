# Gobzigh Integration Configuration Example

## Installation

1. Copy the `gobzigh` folder from `custom_components/` to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant
3. Go to Configuration > Integrations
4. Click "+ ADD INTEGRATION"
5. Search for "Gobzigh" and select it

## Configuration

When adding the integration, you will be prompted to enter:

- **User ID**: Your 24-character Gobzigh User ID (e.g., `665854859c2ad80012bb752d`)

## Device Discovery

After successful setup:

1. The integration will automatically discover your devices
2. Each device will appear in the "Discovered" section of the Integrations page
3. Click "CONFIGURE" on each device you want to add
4. Customize the device name, area, and other settings as needed
5. Click "SUBMIT" to add the device

## Supported Device Types

### Liquid Level Sensors (WLSV0)

Creates the following entities:

#### Sensors:
- **Liquid Level** (cm) - Raw sensor reading
- **Tank Height** (m) - Physical tank height
- **Tank Width** (m) - Physical tank width  
- **Tank Length** (m) - Physical tank length
- **Sensor Distance** (m) - Distance from sensor to tank top
- **Water Height** (m) - Calculated water height in tank
- **Current Volume** (m³) - Current water volume
- **Max Volume** (m³) - Maximum tank capacity
- **Percentage** (%) - Fill percentage
- **Connection Status** - Device connectivity

#### Switches:
- **Relay Switch** - Control device relay (if equipped)

## Device Information

Each device provides:
- **Manufacturer**: Gobzigh
- **Model**: Device model code (e.g., WLSV0)
- **Firmware Version**: Current firmware version
- **MAC Address**: Used to combine devices from other integrations

## Troubleshooting

### No Devices Found

If you receive "No devices were retrieved" error:
1. Verify your User ID is exactly 24 characters
2. Check your internet connection
3. Ensure the Gobzigh servers are online
4. Try refreshing the integration from the options menu

### Device Not Updating

1. Check the device connection status sensor
2. Verify device has internet connectivity
3. Check Home Assistant logs for API errors
4. Try reloading the integration

### Icons Not Showing

The integration includes local fallback icons. If they don't appear:
1. Restart Home Assistant after installation
2. Clear your browser cache
3. Check Home Assistant logs for HTTP errors

## API Information

The integration uses these endpoints:
- Device List: `https://test.autobayt.com/v1/level-sensor-device?user_id={user_id}`
- Device Detail: `https://test.autobayt.com/v1/level-sensor-device?device_id={device_id}`
- Relay Control: `https://test.autobayt.com/v1/level-sensor-device/relay`

Update interval: 290 seconds (configurable in future versions)

## Support

For issues and feature requests:
- GitHub: https://github.com/RASBR/home-assistant-gobzigh
- Issues: https://github.com/RASBR/home-assistant-gobzigh/issues
