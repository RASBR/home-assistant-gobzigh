"""Device management for Gobzigh integration."""
from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class GobzighDeviceManager:
    """Manage Gobzigh devices in the device registry."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the device manager."""
        self.hass = hass
        self._device_registry = dr.async_get(hass)

    async def async_register_device(
        self, 
        device_id: str, 
        device_data: Dict[str, Any]
    ) -> dr.DeviceEntry:
        """Register or update a device in the registry."""
        
        device_name = device_data.get("name", f"Gobzigh {device_data.get('model_name', 'Device')}")
        model_name = device_data.get("model_name", "Unknown")
        firmware_version = device_data.get("firmware_version", "Unknown")
        
        # Use MAC address for device connections to combine devices
        connections = {("mac", device_id)}
        
        # Register device
        device = self._device_registry.async_get_or_create(
            config_entry_id=None,  # Will be set when entities are created
            connections=connections,
            identifiers={(DOMAIN, device_id)},
            manufacturer="Gobzigh",
            name=device_name,
            model=model_name,
            sw_version=firmware_version,
        )
        
        _LOGGER.debug(
            "Registered device %s (%s) with MAC %s",
            device_name,
            model_name,
            device_id
        )
        
        return device

    async def async_update_device(
        self,
        device_id: str,
        device_data: Dict[str, Any]
    ) -> None:
        """Update device information."""
        
        device = self._device_registry.async_get_device(
            identifiers={(DOMAIN, device_id)},
            connections={("mac", device_id)}
        )
        
        if device:
            updates = {}
            
            # Update firmware version if changed
            firmware_version = device_data.get("firmware_version")
            if firmware_version and device.sw_version != firmware_version:
                updates["sw_version"] = firmware_version
            
            # Update name if changed
            device_name = device_data.get("name")
            if device_name and device.name != device_name:
                updates["name"] = device_name
                
            if updates:
                self._device_registry.async_update_device(device.id, **updates)
                _LOGGER.debug("Updated device %s with %s", device_id, updates)

    def get_device_by_mac(self, mac_address: str) -> dr.DeviceEntry | None:
        """Get device by MAC address."""
        return self._device_registry.async_get_device(
            connections={("mac", mac_address)}
        )
