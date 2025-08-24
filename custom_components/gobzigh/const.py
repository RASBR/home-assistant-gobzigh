"""Constants for the Gobzigh integration."""
from typing import Final

DOMAIN: Final = "gobzigh"

# API Configuration
USER_DEVICE_LIST_URL: Final = "https://test.autobayt.com/v1/level-sensor-device?user_id="
DEVICE_DETAIL_URL: Final = "https://test.autobayt.com/v1/level-sensor-device?device_id="

# Device Types Configuration
DEVICE_TYPES: Final = [
    {
        "device_type_code": "WLSV0",
        "type_info": {
            "device_type_name": "Liquid Level",
            "device_generation": "V0"
        },
        "docs_url": "https://github.com/RASBR/home-assistant-gobzigh/wiki/liquid-level-sensor"
    },
    {
        "device_type_code": "OTHV0", 
        "type_info": {
            "device_type_name": "Other",
            "device_generation": "V0"
        },
        "docs_url": "https://github.com/RASBR/home-assistant-gobzigh/wiki/other-devices"
    },
]

# Configuration Keys
CONF_USER_ID: Final = "user_id"

# Update Intervals
DEFAULT_SCAN_INTERVAL: Final = 290  # seconds

# Device Classes and Units
UNIT_PERCENTAGE: Final = "%"
UNIT_METERS: Final = "m"
UNIT_CUBIC_METERS: Final = "m³"
UNIT_CENTIMETERS: Final = "cm"

# Entity Keys
ATTR_RELAY_STATE: Final = "relay_state"
ATTR_CONNECTION_STATUS: Final = "connection_status"
ATTR_POWER_ON_STATE: Final = "power_on_state"
ATTR_IS_UPDATING: Final = "is_updating"
ATTR_DEVICE_ID: Final = "device_id"
ATTR_NAME: Final = "name"
ATTR_FIRMWARE_VERSION: Final = "firmware_version"
ATTR_MODEL_NAME: Final = "model_name"
ATTR_AP_IP: Final = "ap_ip"
ATTR_LOC_ID: Final = "loc_id"
ATTR_USER_ID: Final = "user_id"
ATTR_SETTINGS: Final = "settings"
ATTR_ROOM_NAME: Final = "room_name"
ATTR_CONSUMPTION: Final = "consumption"
ATTR_NEXT_FIRMWARE: Final = "next_firmware"
ATTR_CONNECTED: Final = "connected"

# Settings Keys
SETTINGS_UNIT: Final = "unit"
SETTINGS_LOG_DUR: Final = "log_dur"
SETTINGS_O_RELAY: Final = "o_relay"
SETTINGS_C_RELAY: Final = "c_relay"
SETTINGS_HAS_RELAY: Final = "has_relay"
SETTINGS_IS_AUTO: Final = "is_auto"
SETTINGS_HEIGHT: Final = "height"
SETTINGS_WIDTH: Final = "width"
SETTINGS_LENGTH: Final = "length"
SETTINGS_S_DIST: Final = "s_dist"
SETTINGS_LIQUID_TYPE: Final = "liquid_type"
