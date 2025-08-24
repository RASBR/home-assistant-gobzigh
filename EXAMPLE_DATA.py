# Example API Response Data for Documentation
# This file contains randomized example data for documentation purposes only
# DO NOT use these IDs in production - they are for example purposes only

EXAMPLE_USER_ID = "507f1f77bcf86cd799439011"

EXAMPLE_DEVICE_LIST_RESPONSE = [
    {
        "sensor_val": 75,
        "relay_state": False,
        "room_id": "507f191e810c19729de860ea",
        "connection_status": True,
        "power_on_state": "",
        "is_updating": False,
        "device_id": "a1b2c3d4e5f6",
        "name": "Garden Tank",
        "firmware_version": "1.1.9",
        "model_name": "WLSV0",
        "ap_ip": "192.168.1.100",
        "loc_id": "507f1f77bcf86cd799439011",
        "user_id": "507f1f77bcf86cd799439011",
        "connected": "2025-08-24T10:15:30.123Z",
        "next_firmware": [
            {
                "version_name": "1.2.0",
                "file_name": "wlsv0_1.2.0.bin",
                "version_code": 22,
                "require_client_update": False,
                "app_version_code": 1
            }
        ],
        "settings": {
            "unit": 0,
            "log_dur": 900,
            "o_relay": 10,
            "c_relay": 75,
            "has_relay": True,
            "is_auto": False,
            "height": 150,
            "width": 200,
            "length": 300,
            "s_dist": 50,
            "liquid_type": 0
        },
        "room_name": "Garden",
        "consumption": {
            "day": 125,
            "week": 875,
            "month": 3500
        }
    },
    {
        "sensor_val": 42,
        "relay_state": False,
        "room_id": "507f191e810c19729de860ea",
        "connection_status": True,
        "power_on_state": "",
        "is_updating": False,
        "device_id": "f6e5d4c3b2a1",
        "name": "Storage Tank",
        "firmware_version": "1.1.9",
        "model_name": "WLSV0",
        "ap_ip": "192.168.1.101",
        "loc_id": "507f1f77bcf86cd799439011",
        "user_id": "507f1f77bcf86cd799439011",
        "connected": "2025-08-24T10:18:45.456Z",
        "next_firmware": [
            {
                "version_name": "1.2.0",
                "file_name": "wlsv0_1.2.0.bin",
                "version_code": 22,
                "require_client_update": False,
                "app_version_code": 1
            }
        ],
        "settings": {
            "unit": 0,
            "log_dur": 900,
            "o_relay": 10,
            "c_relay": 80,
            "has_relay": False,
            "is_auto": True,
            "height": 250,
            "width": 180,
            "length": 180,
            "s_dist": 30,
            "liquid_type": 0
        },
        "room_name": "Basement",
        "consumption": {
            "day": 45,
            "week": 315,
            "month": 1260
        }
    },
    {
        "sensor_val": 88,
        "relay_state": True,
        "room_id": "507f191e810c19729de860eb",
        "connection_status": False,
        "power_on_state": "",
        "is_updating": False,
        "device_id": "9x8y7z6w5v4u",
        "name": "Backup Tank",
        "firmware_version": "1.1.7",
        "model_name": "WLSV0",
        "ap_ip": "192.168.1.102",
        "loc_id": "507f1f77bcf86cd799439012",
        "user_id": "507f1f77bcf86cd799439011",
        "connected": "2025-08-20T14:22:10.789Z",
        "next_firmware": [
            {
                "version_name": "1.2.0",
                "file_name": "wlsv0_1.2.0.bin",
                "version_code": 22,
                "require_client_update": False,
                "app_version_code": 1
            }
        ],
        "settings": {
            "unit": 0,
            "log_dur": 600,
            "o_relay": 15,
            "c_relay": 85,
            "has_relay": True,
            "is_auto": True,
            "height": 180,
            "width": 150,
            "length": 220,
            "s_dist": 40,
            "liquid_type": 0
        },
        "room_name": "Utility Room",
        "consumption": {
            "day": 0,
            "week": 0,
            "month": 150
        }
    }
]

# Example MAC addresses (randomized for documentation)
EXAMPLE_MAC_ADDRESSES = [
    "a1b2c3d4e5f6",
    "f6e5d4c3b2a1", 
    "9x8y7z6w5v4u",
    "1a2b3c4d5e6f",
    "6f5e4d3c2b1a"
]

# Example User IDs (randomized for documentation)
EXAMPLE_USER_IDS = [
    "507f1f77bcf86cd799439011",
    "507f1f77bcf86cd799439012",
    "507f1f77bcf86cd799439013"
]

# Example Room/Location IDs (randomized for documentation)
EXAMPLE_ROOM_IDS = [
    "507f191e810c19729de860ea",
    "507f191e810c19729de860eb",
    "507f191e810c19729de860ec"
]
