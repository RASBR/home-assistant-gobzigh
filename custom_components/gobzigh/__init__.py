"""The Gobzigh integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_USER_ID
from .coordinator import GobzighCoordinator
from .http import async_setup_http_views

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Gobzigh from a config entry."""
    _LOGGER.debug("Setting up Gobzigh integration")
    
    # Set up HTTP views for static files (icons/logos) - only once for main integration
    if CONF_USER_ID in entry.data:
        await async_setup_http_views(hass)
    
    # Create coordinator
    coordinator = GobzighCoordinator(hass, entry)
    
    # Store coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Start device discovery (only for main integration entry)
    if CONF_USER_ID in entry.data:
        await coordinator.async_start_discovery()
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading Gobzigh integration")
    
    # Unload platforms
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
