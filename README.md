# GOBZIGH Home Assistant Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue.svg)](https://www.home-assistant.io/)

A comprehensive Home Assistant custom integration for GOBZIGH liquid level monitoring devices.

![GOBZIGH Logo](custom_components/gobzigh/static/000_gobzigh_l_512.png)

## Features

🌊 **Liquid Level Monitoring**
- Real-time distance measurements
- Calculated liquid heights and volumes
- Fill percentage monitoring
- Tank dimension tracking

📊 **Consumption Tracking**
- Daily, weekly, and monthly consumption
- Historical data integration
- Efficiency monitoring

🔌 **Device Control**
- Relay control (where supported)
- Automatic and manual modes
- Threshold-based automation

📱 **Multiple Device Support**
- WLSV0 (Liquid Level Sensors)
- OTHV0 (Other device types)
- Automatic device discovery
- MAC address-based device identification

🏠 **Home Assistant Integration**
- Modern config flow setup
- Device registry integration
- Entity registry with proper unique IDs
- Services for advanced control

## Supported Devices

### WLSV0 - Liquid Level Sensor
- **Sensors**: Distance, liquid height, tank volume, fill percentage, consumption
- **Binary Sensors**: Connection status, updating status, relay capabilities
- **Switches**: Relay control (when available)

### OTHV0 - Other Devices  
- Basic device monitoring and control

## Installation

### Method 1: Manual Installation

1. Download or clone this repository
2. Copy the `custom_components/gobzigh` folder to your Home Assistant `custom_components` directory:
   ```
   <config>/custom_components/gobzigh/
   ```
3. Restart Home Assistant
4. Go to **Settings** → **Devices & Services** → **Add Integration**
5. Search for "GOBZIGH" and follow the setup wizard

### Method 2: Using Installation Script

1. Download this repository
2. Run the installation script:
   ```bash
   python3 install_integration.py
   ```
3. Follow the prompts to automatically install to your Home Assistant

## Configuration

### Initial Setup
1. During setup, you'll need your **GOBZIGH User ID** (24-character hexadecimal string)
2. Example: `507f1f77bcf86cd799439011`
3. The integration will automatically discover all devices associated with your account

### Device Discovery
- New devices are automatically discovered
- Each device appears with comprehensive monitoring entities
- Devices can be added individually as needed

## Entities Created

For each device (example: "Pool Tank"), the integration creates:

### Sensors
- `sensor.pool_tank_distance` - Raw distance measurement (cm)
- `sensor.pool_tank_liquid_height` - Calculated liquid height (m)
- `sensor.pool_tank_current_volume` - Current volume (m³)
- `sensor.pool_tank_max_volume` - Maximum tank capacity (m³)
- `sensor.pool_tank_fill_percentage` - Fill level (%)
- `sensor.pool_tank_consumption_day` - Daily consumption (L)
- `sensor.pool_tank_consumption_week` - Weekly consumption (L)
- `sensor.pool_tank_consumption_month` - Monthly consumption (L)
- Device info sensors (firmware, IP address, etc.)

### Binary Sensors
- `binary_sensor.pool_tank_connection_status` - Online/offline status
- `binary_sensor.pool_tank_updating` - Firmware update status
- `binary_sensor.pool_tank_has_relay` - Relay capability indicator
- `binary_sensor.pool_tank_is_auto` - Automatic mode status

### Switches
- `switch.pool_tank_relay` - Relay control (when available)

## Services

### Refresh Device
```yaml
service: gobzigh.refresh_device
data:
  device_id: "a1b2c3d4e5f6"
```

### Control Relay
```yaml
service: gobzigh.control_relay
data:
  device_id: "a1b2c3d4e5f6"
  state: true  # or false
```

## Automation Examples

### Low Level Alert
```yaml
automation:
  - alias: "Tank Low Level Alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.pool_tank_fill_percentage
      below: 20
    action:
      service: notify.notify
      data:
        message: "Pool tank is low ({{ states('sensor.pool_tank_fill_percentage') }}%)"
```

### Auto-refill System
```yaml
automation:
  - alias: "Auto Refill Tank"
    trigger:
      platform: numeric_state
      entity_id: sensor.pool_tank_fill_percentage
      below: 30
    condition:
      condition: state
      entity_id: binary_sensor.pool_tank_connection_status
      state: 'on'
    action:
      service: switch.turn_on
      entity_id: switch.pool_tank_relay
```

## API Information

This integration connects to GOBZIGH cloud services at:
- **Base URL**: `https://test.autobayt.com/v1/level-sensor-device`
- **Update Interval**: 5 minutes (configurable)
- **Authentication**: User ID-based (no tokens required)

## Requirements

- Home Assistant 2024.1+
- Internet connection for device communication
- GOBZIGH account with registered devices

## Troubleshooting

### No Devices Found
- Verify your User ID is correct (24 characters)
- Check that devices are online in the GOBZIGH app
- Ensure internet connectivity

### Entities Not Updating
- Check Home Assistant logs for errors
- Verify device connectivity
- Try refreshing device data using the service

### Device Offline
- Check device power and network connection
- Verify device status in GOBZIGH mobile app
- Check firewall/network restrictions

## Development

### Project Structure
```
custom_components/gobzigh/
├── __init__.py              # Integration setup
├── manifest.json            # Integration metadata
├── config_flow.py           # Setup flow
├── const.py                 # Constants
├── api.py                   # API client
├── coordinator.py           # Data coordinator
├── sensor.py                # Sensor platform
├── binary_sensor.py         # Binary sensor platform
├── switch.py                # Switch platform
├── services.py              # Custom services
└── static/                  # Assets and icons
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/RASBR/home-assistant-gobzigh/issues)
- **Discussions**: [GitHub Discussions](https://github.com/RASBR/home-assistant-gobzigh/discussions)
- **Documentation**: Check the [integration overview](INTEGRATION_OVERVIEW.md)

## Changelog

### v1.0.0 (2025-08-22)
- Initial release
- Support for WLSV0 and OTHV0 devices
- Complete sensor suite for liquid level monitoring
- Device discovery and management
- Relay control capabilities
- Custom services integration
- Comprehensive error handling

---

**Made with ❤️ for the Home Assistant community**
