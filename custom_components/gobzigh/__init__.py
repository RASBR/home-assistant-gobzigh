"""The GOBZIGH integration."""
from __future__ import annotations

import logging
import os
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr
from homeassistant.components.http import StaticPathConfig

from .const import DOMAIN, CONF_USER_ID
from .coordinator import GobzighDataUpdateCoordinator
from .api import GobzighAPI
from .services import async_setup_services, async_unload_services
from .icons import get_device_icon

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up GOBZIGH from a config entry."""
    user_id = entry.data[CONF_USER_ID]
    
    # Initialize the API
    api = GobzighAPI(user_id)
    
    # Test the connection
    try:
        devices = await api.async_get_devices()
        if devices is None:
            raise ConfigEntryNotReady("Unable to connect to GOBZIGH API")
    except Exception as err:
        _LOGGER.error("Error connecting to GOBZIGH API: %s", err)
        raise ConfigEntryNotReady("Unable to connect to GOBZIGH API") from err

    # Create data update coordinator
    coordinator = GobzighDataUpdateCoordinator(hass, api)
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator in hass data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Register static path for images
    static_path = os.path.join(os.path.dirname(__file__), "static")
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            url_path=f"/api/{DOMAIN}/static",
            path=static_path,
            cache_headers=False
        )
    ])

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Set up services
    await async_setup_services(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload services
    await async_unload_services(hass)
    
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


def get_device_info(device_data: dict[str, Any]) -> dict[str, Any]:
    """Get device info for Home Assistant device registry."""
    model_name = device_data.get("model_name", "")
    device_info = {
        "identifiers": {(DOMAIN, device_data["device_id"])},
        "name": device_data["name"],
        "manufacturer": "GOBZIGH",
        "model": model_name,
        "sw_version": device_data.get("firmware_version"),
        "connections": {(dr.CONNECTION_NETWORK_MAC, device_data["device_id"])},
        "configuration_url": f"http://{device_data.get('ap_ip', '')}" if device_data.get("ap_ip") else None,
    }
    
    # Add device icon
    icon_url = get_device_icon(model_name)
    if icon_url:
        device_info["configuration_url"] = device_info.get("configuration_url") or icon_url
        
    return device_info
