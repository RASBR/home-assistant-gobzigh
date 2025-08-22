"""Constants for the GOBZIGH integration."""

# Integration
DOMAIN = "gobzigh"
INTEGRATION_NAME = "GOBZIGH"

# Configuration
CONF_USER_ID = "user_id"

# API
API_BASE_URL = "https://test.autobayt.com/v1"
USER_DEVICE_LIST_URL = f"{API_BASE_URL}/level-sensor-device"
DEVICE_URL = f"{API_BASE_URL}/level-sensor-device"

# Polling
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes
MIN_SCAN_INTERVAL = 60       # 1 minute

# Device Types
DEVICE_TYPES = [
    {
        "device_type_code": "WLSV0",
        "type_info": {
            "device_type_name": "Liquid Level",
            "device_generation": "V0"
        },
        "docs_url": "https://github.com/RASBR/home-assistant-gobzigh/blob/main/docs/WLSV0.md"
    },
    {
        "device_type_code": "OTHV0", 
        "type_info": {
            "device_type_name": "Other",
            "device_generation": "V0"
        },
        "docs_url": "https://github.com/RASBR/home-assistant-gobzigh/blob/main/docs/OTHV0.md"
    }
]

# Entities
LIQUID_TYPE_MAP = {
    0: "Water",
    1: "Diesel",
    2: "Gasoline",
    3: "Oil",
    4: "Other"
}

UNIT_MAP = {
    0: "cm",
    1: "m",
    2: "inches",
    3: "feet"
}

# Error messages
ERROR_NO_DEVICES = "No devices were retrieved. Please check that you have provided the correct User ID, or that the server is online and you have internet access."
ERROR_INVALID_USER_ID = "Invalid User ID format. Please provide a valid 24-character User ID."
ERROR_CONNECTION = "Unable to connect to GOBZIGH servers. Please check your internet connection."
ERROR_INVALID_RESPONSE = "Invalid response from GOBZIGH servers."
