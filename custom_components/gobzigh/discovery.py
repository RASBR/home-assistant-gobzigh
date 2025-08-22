"""Device discovery for GOBZIGH integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import discovery_flow
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

from .const import DOMAIN, DEVICE_TYPES
from .coordinator import GobzighDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class GobzighDeviceDiscovery:
    """Handle device discovery for GOBZIGH integration."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize device discovery."""
        self.hass = hass
        self.config_entry = config_entry
        self._discovered_devices: set[str] = set()

    async def async_discover_devices(self) -> None:
        """Discover new devices."""
        coordinator: GobzighDataUpdateCoordinator = self.hass.data[DOMAIN][
            self.config_entry.entry_id
        ]

        # Get current devices from coordinator
        current_devices = set(coordinator.data.keys()) if coordinator.data else set()
        
        # Find new devices
        new_devices = current_devices - self._discovered_devices
        
        if new_devices:
            _LOGGER.info("Discovered %d new GOBZIGH devices", len(new_devices))
            
            for device_id in new_devices:
                device_data = coordinator.data.get(device_id, {})
                await self._async_create_device_discovery(device_id, device_data)
                
            # Update discovered devices set
            self._discovered_devices.update(new_devices)

    async def _async_create_device_discovery(
        self, device_id: str, device_data: dict[str, Any]
    ) -> None:
        """Create discovery entry for a device."""
        model_name = device_data.get("model_name", "")
        device_name = device_data.get("name", f"GOBZIGH Device {device_id}")
        
        # Get device type info
        device_type_info = next(
            (dt for dt in DEVICE_TYPES if dt["device_type_code"] == model_name),
            {"type_info": {"device_type_name": "Unknown"}, "docs_url": ""}
        )
        
        # Create discovery info
        discovery_info = {
            "device_id": device_id,
            "name": device_name,
            "model": model_name,
            "type_name": device_type_info["type_info"]["device_type_name"],
            "docs_url": device_type_info.get("docs_url", ""),
            "connection_status": device_data.get("connection_status", False),
            "firmware_version": device_data.get("firmware_version", ""),
            "config_entry_id": self.config_entry.entry_id,
        }

        # Start discovery flow
        discovery_flow.async_create_flow(
            self.hass,
            DOMAIN,
            context={"source": "discovery"},
            data=discovery_info,
        )

    @callback
    def async_remove_discovered_device(self, device_id: str) -> None:
        """Remove a device from discovered devices."""
        self._discovered_devices.discard(device_id)

    async def async_get_device_entities(self, device_id: str) -> list[str]:
        """Get list of entities for a device."""
        entity_registry = async_get_entity_registry(self.hass)
        entities = []
        
        for entity in entity_registry.entities.values():
            if (
                entity.platform == DOMAIN and
                entity.unique_id and
                entity.unique_id.startswith(device_id)
            ):
                entities.append(entity.entity_id)
                
        return entities

    async def async_remove_device_entities(self, device_id: str) -> None:
        """Remove all entities for a device."""
        entities = await self.async_get_device_entities(device_id)
        entity_registry = async_get_entity_registry(self.hass)
        
        for entity_id in entities:
            entity_registry.async_remove(entity_id)
            
        _LOGGER.info("Removed %d entities for device %s", len(entities), device_id)
