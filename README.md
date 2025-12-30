# Gobzigh Home Assistant Integration

[![Made with GitHub Copilot & Claude](https://img.shields.io/badge/Made%20with-Copilot%20%26%20Claude-7B68EE?logo=github&logoColor=white&style=flat)](https://github.com/features/copilot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue.svg)](https://www.home-assistant.io/)
![Version](https://img.shields.io/github/v/release/RASBR/home-assistant-gobzigh)
![Last Commit](https://img.shields.io/github/last-commit/RASBR/home-assistant-gobzigh?date_format=dd-mmm-yyyy)
![Stars](https://img.shields.io/github/stars/RASBR/home-assistant-gobzigh)
![Forks](https://img.shields.io/github/forks/RASBR/home-assistant-gobzigh)
![Issues](https://img.shields.io/github/issues/RASBR/home-assistant-gobzigh)

A comprehensive Home Assistant custom integration for Gobzigh liquid level monitoring devices with automatic device discovery and seamless integration.

## ✨ Features

- 🌊 **Real-time Liquid Level Monitoring** - Distance measurements, liquid heights, and volume calculations
- 📊 **Smart Consumption Tracking** - Daily, weekly, and monthly usage statistics
- 🔌 **Device Control** - Relay switches with automatic and manual modes
- 🔍 **Automatic Device Discovery** - Just like Shelly integration - devices appear automatically for easy addition
- � **Multiple Device Support** - WLSV0 (Liquid Level) and OTHV0 (Other) device types
- 🏠 **Modern Home Assistant Integration** - Config flow setup, device registry, proper unique IDs
- 🖼️ **Custom Icons & Logos** - Local fallback icons included for offline operation
- 🔗 **Device Consolidation** - Automatically combines devices by MAC address across integrations

## 📱 Supported Devices

### WLSV0 - Liquid Level Sensor
Creates comprehensive monitoring with:

**Sensors:**
- Liquid Level (cm) - Raw sensor reading
- Tank Height/Width/Length (m) - Physical dimensions
- Sensor Distance (m) - Mounting distance
- Water Height (m) - Calculated liquid level
- Current/Max Volume (m³) - Volume calculations
- Fill Percentage (%) - Tank fill level
- Connection Status - Device connectivity

**Switches:**
- Relay Control - Device relay management (if equipped)

### OTHV0 - Other Devices
Basic monitoring and control for additional device types.

## 🚀 Installation

### Method 1: Manual Installation (Recommended)

1. Download or clone this repository
2. Copy the `custom_components/gobzigh` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant
4. The integration is now ready to configure!

### Method 2: Git Clone
```bash
cd /config/custom_components
git clone https://github.com/RASBR/home-assistant-gobzigh.git gobzigh
```

### Directory Structure
After installation, you should have:
```
config/
  custom_components/
    gobzigh/
      __init__.py
      manifest.json
      config_flow.py
      coordinator.py
      sensor.py
      switch.py
      const.py
      icon.png
      logo.png
      translations/
        en.json
```

## ⚙️ Configuration

### Initial Setup

1. Go to **Configuration** → **Integrations**
2. Click **"+ ADD INTEGRATION"**
3. Search for **"Gobzigh"** and select it
4. Enter your **24-character User ID** (e.g., `507f1f77bcf86cd799439011`)
5. Click **"SUBMIT"**

### Device Discovery & Addition

After successful setup:

1. **Automatic Discovery**: Your devices will automatically appear in the "Discovered" section
2. **Device Information**: Each discovered device shows:
   - Gobzigh logo
   - Model name (e.g., WLSV0)
   - Three-dot menu with documentation link
   - "IGNORE" and "ADD" buttons
3. **Adding Devices**: Click "ADD" on devices you want to monitor
4. **Configuration**: Customize device name, area, labels, and other settings
5. **Completion**: Click "SUBMIT" to create the device and its entities

## 📊 Entity Details

### Liquid Level Device Entities

| Entity | Type | Unit | Description |
|--------|------|------|-------------|
| `sensor.{name}` | Sensor | cm | Raw distance reading from sensor |
| `sensor.{name}_height` | Sensor | m | Physical tank height |
| `sensor.{name}_width` | Sensor | m | Physical tank width |
| `sensor.{name}_length` | Sensor | m | Physical tank length |
| `sensor.{name}_sensor_distance` | Sensor | m | Sensor mounting distance |
| `sensor.{name}_water_height` | Sensor | m | Calculated liquid height |
| `sensor.{name}_current_volume` | Sensor | m³ | Current liquid volume |
| `sensor.{name}_max_volume` | Sensor | m³ | Maximum tank capacity |
| `sensor.{name}_percentage` | Sensor | % | Fill percentage |
| `sensor.{name}_connected` | Sensor | - | Connection status |
| `switch.{name}_switch` | Switch | - | Relay control (if available) |

### Attributes

Each main sensor includes comprehensive attributes:
- Device settings (relay thresholds, dimensions, etc.)
- Consumption data (daily, weekly, monthly)
- Firmware information
- Connection timestamps
- Room and location IDs

## 🔧 Advanced Features

### Device Consolidation
The integration automatically combines devices with the same MAC address from other integrations in the Home Assistant device registry.

### Custom Icons
Local fallback icons are included and automatically served by Home Assistant for offline operation.

### API Integration
- **Update Interval**: 290 seconds (optimized for device battery life)
- **Endpoints**: Automatic API endpoint management
- **Error Handling**: Comprehensive error handling with user-friendly messages

## 🔍 Troubleshooting

### Common Issues

**"No devices were retrieved" Error:**
- Verify your User ID is exactly 24 characters
- Check internet connectivity
- Confirm Gobzigh servers are online
- Try the options/configuration menu to update User ID

**Device Not Updating:**
- Check the connection status sensor
- Verify device internet connectivity
- Review Home Assistant logs for API errors
- Try reloading the integration

**Icons Not Displaying:**
- Restart Home Assistant after installation
- Clear browser cache
- Check Home Assistant logs for HTTP view errors

**Discovery Not Working:**
- Wait a few minutes for initial API calls
- Check User ID format (24 characters)
- Reload integration from Configuration → Integrations

### Logging

Enable debug logging by adding to `configuration.yaml`:
```yaml
logger:
  logs:
    custom_components.gobzigh: debug
```

## 🛠️ Development

### API Endpoints
- Device List: `https://test.gobzigh.com/v1/level-sensor-device?user_id={user_id}`
- Device Detail: `https://test.gobzigh.com/v1/level-sensor-device?device_id={device_id}`
- Relay Control: `https://test.gobzigh.com/v1/level-sensor-device/relay`

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues, questions, or feature requests:
- **GitHub Issues**: [Create an Issue](https://github.com/RASBR/home-assistant-gobzigh/issues)
- **Documentation**: [Configuration Guide](CONFIGURATION.md)
- **Repository**: [home-assistant-gobzigh](https://github.com/RASBR/home-assistant-gobzigh)

---

**Made with ❤️ for the Home Assistant Community**

### Method 1: Manual Installation

1. Download or clone this repository
2. Copy the `custom_components/gobzigh` folder to your Home Assistant `custom_components` directory:
   ```
   <config>/custom_components/gobzigh/
   ```
3. Restart Home Assistant
4. Go to **Settings** → **Devices & Services** → **Add Integration**
5. Search for "GOBZIGH" and follow the setup wizard

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
- **Base URL**: `https://test.gobzigh.com/v1/level-sensor-device`
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
