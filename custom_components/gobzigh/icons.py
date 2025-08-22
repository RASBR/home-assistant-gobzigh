"""Icon utilities for GOBZIGH integration."""
from __future__ import annotations

from .const import LIQUID_TYPE_MAP, DOMAIN


def get_liquid_level_icon(liquid_type: int, percentage: float) -> str:
    """Get appropriate icon based on liquid type and level."""
    liquid_name = LIQUID_TYPE_MAP.get(liquid_type, "water").lower()
    
    # Determine level range
    if percentage >= 80:
        level = "5"
    elif percentage >= 60:
        level = "4"
    elif percentage >= 40:
        level = "3"
    elif percentage >= 20:
        level = "2"
    elif percentage >= 5:
        level = "1"
    else:
        level = "0"
    
    # Map to appropriate icon
    if liquid_name == "water":
        return f"/api/{DOMAIN}/static/water_{level}.png"
    elif liquid_name in ["diesel", "gasoline", "oil"]:
        return f"/api/{DOMAIN}/static/diesel_{level}.png"
    else:
        return "mdi:gauge"


def get_device_icon(model_name: str) -> str:
    """Get device icon based on model."""
    if model_name == "WLSV0":
        return f"/api/{DOMAIN}/static/gobzigh-1.png"
    else:
        return f"/api/{DOMAIN}/static/gobzigh-2.png"


def get_brand_icons() -> dict[str, str]:
    """Get brand icon mappings."""
    return {
        "icon": f"/api/{DOMAIN}/static/icon.png",
        "dark_icon": f"/api/{DOMAIN}/static/dark_icon.png",
        "logo": f"/api/{DOMAIN}/static/logo.png",
        "dark_logo": f"/api/{DOMAIN}/static/dark_logo.png",
        "gobzigh_logo_1": f"/api/{DOMAIN}/static/gobzigh-1.png",
        "gobzigh_logo_2": f"/api/{DOMAIN}/static/gobzigh-2.png",
        "autobayt_logo_1": f"/api/{DOMAIN}/static/autobayt-logo-1.png",
        "autobayt_logo_3": f"/api/{DOMAIN}/static/autobayt-logo-3.png",
        "banner_level_white": f"/api/{DOMAIN}/static/banner-level-white.png",
        "home_assistant_1": f"/api/{DOMAIN}/static/home_assistant_(1).png",
        "home_assistant_alt": f"/api/{DOMAIN}/static/home_assistant_alt.png",
    }
