"""Services for GOBZIGH integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .coordinator import GobzighDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

SERVICE_REFRESH_DEVICE = "refresh_device"
SERVICE_CONTROL_RELAY = "control_relay"

SERVICE_REFRESH_DEVICE_SCHEMA = vol.Schema({
    vol.Required("device_id"): cv.string,
})

SERVICE_CONTROL_RELAY_SCHEMA = vol.Schema({
    vol.Required("device_id"): cv.string,
    vol.Required("state"): cv.boolean,
})


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for GOBZIGH integration."""

    async def async_refresh_device(call: ServiceCall) -> None:
        """Refresh a specific device."""
        device_id = call.data["device_id"]
        
        # Find the coordinator for this device
        coordinator = None
        for entry_id, coord in hass.data[DOMAIN].items():
            if isinstance(coord, GobzighDataUpdateCoordinator):
                if device_id in coord.data:
                    coordinator = coord
                    break
        
        if not coordinator:
            _LOGGER.error("Device %s not found in any coordinator", device_id)
            return
            
        await coordinator.async_request_refresh()
        _LOGGER.info("Refreshed device %s", device_id)

    async def async_control_relay(call: ServiceCall) -> None:
        """Control device relay."""
        device_id = call.data["device_id"]
        state = call.data["state"]
        
        # Find the coordinator for this device
        coordinator = None
        for entry_id, coord in hass.data[DOMAIN].items():
            if isinstance(coord, GobzighDataUpdateCoordinator):
                if device_id in coord.data:
                    coordinator = coord
                    break
        
        if not coordinator:
            _LOGGER.error("Device %s not found in any coordinator", device_id)
            return
            
        success = await coordinator.async_control_relay(device_id, state)
        if success:
            _LOGGER.info("Successfully set relay state to %s for device %s", state, device_id)
        else:
            _LOGGER.error("Failed to set relay state for device %s", device_id)

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH_DEVICE,
        async_refresh_device,
        schema=SERVICE_REFRESH_DEVICE_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CONTROL_RELAY,
        async_control_relay,
        schema=SERVICE_CONTROL_RELAY_SCHEMA,
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload services for GOBZIGH integration."""
    hass.services.async_remove(DOMAIN, SERVICE_REFRESH_DEVICE)
    hass.services.async_remove(DOMAIN, SERVICE_CONTROL_RELAY)
