# GOBZIGH Home Assistant Integration

## Overview

This is a comprehensive Home Assistant custom integration for GOBZIGH liquid level monitoring devices. The integration follows Home Assistant's latest best practices and provides a complete solution for monitoring and controlling GOBZIGH devices.

## Features

✅ **Full Home Assistant Integration**
- Config flow setup via UI
- Device discovery and management
- Entity registry integration
- Options flow for configuration
- Services for device control

✅ **Comprehensive Device Support**
- WLSV0 (Liquid Level) devices
- OTHV0 (Other) devices
- Automatic device type detection
- MAC address-based device identification

✅ **Rich Entity Support**
- Sensor entities with proper device classes and state classes
- Binary sensor entities for status monitoring
- Switch entities for relay control
- Proper unique IDs and naming

✅ **Advanced Features**
- Data update coordinator with proper error handling
- Retry logic for API calls
- Device discovery system
- Service integration
- Icon mapping based on liquid type and levels

## File Structure

```
custom_components/gobzigh/
├── __init__.py              # Main integration setup
├── manifest.json            # Integration metadata
├── const.py                 # Constants and configuration
├── config_flow.py           # Configuration flow
├── api.py                   # API client with error handling
├── coordinator.py           # Data update coordinator
├── sensor.py                # Sensor platform
├── binary_sensor.py         # Binary sensor platform  
├── switch.py                # Switch platform
├── services.py              # Integration services
├── services.yaml            # Service definitions
├── discovery.py             # Device discovery
├── device_tracker.py        # Device management
├── icons.py                 # Icon utilities
├── strings.json             # Translations
├── static/                  # Static assets (logos, icons)
├── README.md                # User documentation
└── examples.md              # Configuration examples
```

## Installation Instructions

1. **Copy Integration Files**
   ```
   Copy the entire 'gobzigh' folder to:
   <config_directory>/custom_components/gobzigh/
   ```

2. **Restart Home Assistant**
   - Restart your Home Assistant instance

3. **Add Integration**
   - Go to Configuration → Integrations
   - Click "Add Integration"
   - Search for "GOBZIGH"
   - Follow the setup wizard

4. **Enter User ID**
   - Provide your 24-character GOBZIGH User ID
   - The integration will automatically discover your devices

## Key Technical Features

### API Client (`api.py`)
- Robust error handling with custom exceptions
- Retry logic for failed requests
- Timeout management
- Proper session management

### Data Coordinator (`coordinator.py`)
- Efficient data polling every 5 minutes
- Proper error propagation
- Device state management
- Relay control integration

### Configuration Flow (`config_flow.py`)
- User ID validation (24-character hex string)
- Device discovery during setup
- Reconfiguration support
- Options flow for scan interval

### Entity Platforms
- **Sensors**: Distance, dimensions, volumes, consumption, diagnostics
- **Binary Sensors**: Connection status, update status, capabilities
- **Switches**: Relay control with availability checking

### Device Management
- Proper device registry integration
- MAC address connections for device combination
- Firmware version tracking
- IP address configuration URLs

## API Integration

**Base URL**: `https://test.autobayt.com/v1/level-sensor-device`

**Endpoints Used**:
- `GET ?user_id={user_id}` - Get all user devices
- `GET ?device_id={device_id}` - Get specific device data

**Authentication**: User ID-based (no tokens required)

## Entity Examples

For a device named "Pool Tank" with ID "a1b2c3d4e5f6":

```yaml
# Main sensor
sensor.pool_tank_distance

# Calculated sensors  
sensor.pool_tank_liquid_height
sensor.pool_tank_current_volume
sensor.pool_tank_fill_percentage

# Diagnostic sensors
sensor.pool_tank_firmware_version
sensor.pool_tank_ip_address

# Status sensors
binary_sensor.pool_tank_connection_status
binary_sensor.pool_tank_updating

# Controls
switch.pool_tank_relay
```

## Services

```yaml
# Refresh specific device
service: gobzigh.refresh_device
data:
  device_id: "a1b2c3d4e5f6"

# Control relay
service: gobzigh.control_relay  
data:
  device_id: "a1b2c3d4e5f6"
  state: true
```

## Error Handling

The integration includes comprehensive error handling:

- **Connection errors**: Retry logic with exponential backoff
- **Authentication errors**: Clear error messages for invalid User IDs
- **API errors**: Proper error propagation and logging
- **Device unavailable**: Proper availability status for entities

## Future Enhancements

Planned improvements:
- Relay control API implementation (currently placeholder)
- Additional device type support
- Historical data integration
- Advanced automation triggers
- Mobile app integration

## Development Notes

This integration was built following Home Assistant's integration development best practices:
- Async/await patterns throughout
- Proper type hints
- Comprehensive error handling
- Entity registry integration
- Device registry integration
- Translation support
- Service integration

The code is structured for easy maintenance and extension to support additional GOBZIGH device types and features.
