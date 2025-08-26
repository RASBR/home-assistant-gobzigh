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
    
    # Set up HTTP views for brand images (fallback when CDN fails) - only once
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
    _LOGGER.debug("Unloading Gobzigh integration entry: %s", entry.entry_id)
    
    # Check if this is the main integration entry (has user_id)
    if CONF_USER_ID in entry.data:
        _LOGGER.debug("Unloading main integration - cleaning up all devices")
        await _async_cleanup_integration_devices(hass, entry)
    
    # Unload platforms
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()
    
    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove a config entry."""
    _LOGGER.debug("Removing Gobzigh integration entry: %s", entry.entry_id)
    
    # Check if this is the main integration entry (has user_id)
    if CONF_USER_ID in entry.data:
        _LOGGER.debug("Removing main integration - cleaning up all devices")
        await _async_cleanup_integration_devices(hass, entry)
    elif "device_id" in entry.data:
        _LOGGER.debug("Removing device entry - triggering rediscovery")
        await _async_cleanup_device_and_rediscover(hass, entry)


async def _async_cleanup_device_and_rediscover(hass: HomeAssistant, device_entry: ConfigEntry) -> None:
    """Clean up a single device and trigger rediscovery."""
    from homeassistant.helpers import device_registry as dr, entity_registry as er
    from homeassistant.helpers import discovery_flow
    
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)
    
    device_id = device_entry.data.get("device_id")
    if not device_id:
        return
        
    _LOGGER.debug("Cleaning up device: %s", device_id)
    
    # Find the device in device registry
    device = None
    for dev in device_registry.devices.values():
        if any(identifier == (DOMAIN, device_id) for identifier in dev.identifiers):
            device = dev
            break
    
    if device:
        # Remove all entities for this device
        entities = er.async_entries_for_device(entity_registry, device.id)
        for entity in entities:
            if entity.platform == DOMAIN:
                _LOGGER.debug("Removing entity: %s", entity.entity_id)
                entity_registry.async_remove(entity.entity_id)
                
        # Remove the device from device registry
        _LOGGER.debug("Removing device from registry: %s", device.name)
        device_registry.async_remove_device(device.id)
    
    # Find the main integration entry to trigger rediscovery
    main_entry = None
    for entry in hass.config_entries.async_entries(DOMAIN):
        if CONF_USER_ID in entry.data:
            main_entry = entry
            break
    
    if main_entry and main_entry.state.name == "LOADED":
        # Get the coordinator and trigger rediscovery
        coordinator = hass.data[DOMAIN].get(main_entry.entry_id)
        if coordinator:
            # Reset device discovery status so it can be rediscovered
            coordinator.reset_device_discovery(device_id)
            
            # Get device data from coordinator
            device_data = None
            if coordinator.data and "user_devices" in coordinator.data:
                for device in coordinator.data["user_devices"]:
                    if device.get("device_id") == device_id:
                        device_data = device
                        break
            
            if device_data:
                _LOGGER.debug("Triggering rediscovery for device: %s", device_id)
                # Create new discovery flow
                discovery_flow.async_create_flow(
                    hass,
                    DOMAIN,
                    context={"source": "discovery"},
                    data={
                        "device_id": device_id,
                        "device_data": device_data,
                        "user_id": main_entry.data.get(CONF_USER_ID),
                    },
                )


async def _async_cleanup_integration_devices(hass: HomeAssistant, main_entry: ConfigEntry) -> None:
    """Clean up all devices and device entries for this integration."""
    from homeassistant.helpers import device_registry as dr, entity_registry as er
    
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)
    
    # Find all devices belonging to this integration
    integration_devices = []
    for device in device_registry.devices.values():
        if any(identifier[0] == DOMAIN for identifier in device.identifiers):
            integration_devices.append(device)
            
    _LOGGER.debug("Found %d devices to clean up", len(integration_devices))
    
    # Remove all entities for each device first
    for device in integration_devices:
        entities = er.async_entries_for_device(entity_registry, device.id)
        for entity in entities:
            if entity.platform == DOMAIN:
                _LOGGER.debug("Removing entity: %s", entity.entity_id)
                entity_registry.async_remove(entity.entity_id)
                
        # Remove the device
        _LOGGER.debug("Removing device: %s", device.name)
        device_registry.async_remove_device(device.id)
    
    # Find and remove all device config entries for this integration
    user_id = main_entry.data.get(CONF_USER_ID)
    if user_id:
        entries_to_remove = []
        for entry in hass.config_entries.async_entries(DOMAIN):
            # Remove device entries (those without user_id but with device_id)
            if (entry.entry_id != main_entry.entry_id and 
                CONF_USER_ID not in entry.data and 
                "device_id" in entry.data):
                entries_to_remove.append(entry)
                
        for entry in entries_to_remove:
            _LOGGER.debug("Removing device config entry: %s", entry.data.get("device_id"))
            await hass.config_entries.async_remove(entry.entry_id)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
