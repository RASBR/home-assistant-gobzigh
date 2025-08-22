"""Device tracker utilities for GOBZIGH integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class GobzighDeviceTracker:
    """Track and manage GOBZIGH devices."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize device tracker."""
        self.hass = hass
        self.device_registry = dr.async_get(hass)

    def async_get_or_create_device(self, device_data: dict[str, Any]) -> dr.DeviceEntry:
        """Get or create a device entry."""
        device_id = device_data["device_id"]
        
        # Try to find existing device
        device = self.device_registry.async_get_device(
            identifiers={(DOMAIN, device_id)},
            connections={(dr.CONNECTION_NETWORK_MAC, device_id)}
        )
        
        if device:
            # Update existing device
            self.device_registry.async_update_device(
                device.id,
                name=device_data.get("name"),
                sw_version=device_data.get("firmware_version"),
                configuration_url=f"http://{device_data.get('ap_ip', '')}" if device_data.get("ap_ip") else None,
            )
            return device
        else:
            # Create new device
            device = self.device_registry.async_get_or_create(
                config_entry_id="",  # Will be set by the coordinator
                identifiers={(DOMAIN, device_id)},
                connections={(dr.CONNECTION_NETWORK_MAC, device_id)},
                name=device_data.get("name", f"GOBZIGH {device_id}"),
                manufacturer="GOBZIGH",
                model=device_data.get("model_name", "Unknown"),
                sw_version=device_data.get("firmware_version"),
                configuration_url=f"http://{device_data.get('ap_ip', '')}" if device_data.get("ap_ip") else None,
            )
            return device

    def async_remove_device(self, device_id: str) -> None:
        """Remove a device from registry."""
        device = self.device_registry.async_get_device(
            identifiers={(DOMAIN, device_id)}
        )
        if device:
            self.device_registry.async_remove_device(device.id)
            _LOGGER.info("Removed device %s from registry", device_id)

    def async_get_device_by_id(self, device_id: str) -> dr.DeviceEntry | None:
        """Get device by ID."""
        return self.device_registry.async_get_device(
            identifiers={(DOMAIN, device_id)}
        )

    def async_update_device_info(self, device_id: str, device_data: dict[str, Any]) -> None:
        """Update device information."""
        device = self.async_get_device_by_id(device_id)
        if device:
            self.device_registry.async_update_device(
                device.id,
                name=device_data.get("name"),
                sw_version=device_data.get("firmware_version"),
                configuration_url=f"http://{device_data.get('ap_ip', '')}" if device_data.get("ap_ip") else None,
            )
