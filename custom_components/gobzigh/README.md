# GOBZIGH Home Assistant Integration

A custom Home Assistant integration for GOBZIGH liquid level monitoring devices.

## Features

- **Multiple Device Support**: Supports WLSV0 (Liquid Level) and OTHV0 (Other) device types
- **Real-time Monitoring**: Track liquid levels, consumption, and device status
- **Relay Control**: Control device relays (where available)
- **Rich Entities**: Comprehensive sensor data including:
  - Distance measurements
  - Tank dimensions and calculated volumes
  - Fill percentages
  - Connection status and diagnostics
  - Daily/weekly/monthly consumption tracking
- **Device Discovery**: Automatic discovery of new devices
- **Easy Setup**: Simple configuration via Home Assistant UI

## Installation

### Manual Installation

1. Copy the `gobzigh` folder to your Home Assistant `custom_components` directory:
   ```
   custom_components/
     gobzigh/
   ```

2. Restart Home Assistant

3. Go to **Configuration** > **Integrations** and click **Add Integration**

4. Search for "GOBZIGH" and select it

5. Enter your GOBZIGH User ID (24-character hex string)

## Configuration

### User ID
Your GOBZIGH User ID is a 24-character hexadecimal string that identifies your account. You can find this in your GOBZIGH mobile app or web interface.

Example: `665854859c2ad80012bb752d`

### Device Discovery
Once configured, the integration will automatically discover all devices associated with your User ID. Each device will be added with all relevant sensors and controls.

## Supported Devices

### WLSV0 - Liquid Level Sensor
- **Sensors**: Distance, liquid height, tank volume, fill percentage, consumption
- **Binary Sensors**: Connection status, updating status, relay capability
- **Switches**: Relay control (if available)

### OTHV0 - Other Devices
- Basic device monitoring and control

## Entities

### Sensors
- **Distance**: Raw sensor reading in centimeters
- **Tank Dimensions**: Height, width, length in meters
- **Liquid Height**: Calculated liquid height in meters
- **Volumes**: Current and maximum volume in cubic meters
- **Fill Percentage**: Current fill level as percentage
- **Consumption**: Daily, weekly, and monthly consumption in liters
- **Device Info**: Firmware version, IP address, liquid type

### Binary Sensors
- **Connection Status**: Online/offline status
- **Updating**: Firmware update status
- **Has Relay**: Whether device has relay capability
- **Auto Mode**: Automatic relay control mode

### Switches
- **Relay**: Control device relay (when available)

## Services

### `gobzigh.refresh_device`
Manually refresh data for a specific device.

**Parameters:**
- `device_id` (required): Device MAC address

### `gobzigh.control_relay`
Control device relay state.

**Parameters:**
- `device_id` (required): Device MAC address
- `state` (required): True for on, False for off

## API Information

This integration connects to the GOBZIGH cloud service at `https://test.autobayt.com/v1/level-sensor-device`

**Data Update Frequency**: Every 5 minutes (configurable)

## Troubleshooting

### No Devices Found
- Verify your User ID is correct (24 characters, hexadecimal)
- Check internet connection
- Ensure devices are online and connected to GOBZIGH servers

### Device Not Responding
- Check device connection status in the GOBZIGH app
- Verify device has internet connectivity
- Try the refresh device service

### Entities Not Updating
- Check integration logs in Home Assistant
- Verify API connectivity
- Restart the integration if needed

## Support

For issues and feature requests:
- GitHub: [https://github.com/RASBR/home-assistant-gobzigh](https://github.com/RASBR/home-assistant-gobzigh)

## License

This integration is provided as-is for personal use with GOBZIGH devices.
