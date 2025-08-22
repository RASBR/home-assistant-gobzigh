"""Binary sensor platform for GOBZIGH integration."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import get_device_info
from .const import DOMAIN
from .coordinator import GobzighDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

BINARY_SENSOR_DESCRIPTIONS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="connection_status",
        name="Connection Status",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:wifi",
    ),
    BinarySensorEntityDescription(
        key="is_updating",
        name="Updating",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:update",
    ),
    BinarySensorEntityDescription(
        key="has_relay",
        name="Has Relay",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:electric-switch",
    ),
    BinarySensorEntityDescription(
        key="is_auto",
        name="Auto Mode",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:auto-mode",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up GOBZIGH binary sensors from a config entry."""
    coordinator: GobzighDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for device_id, device_data in coordinator.data.items():
        for description in BINARY_SENSOR_DESCRIPTIONS:
            entities.append(GobzighBinarySensor(coordinator, device_id, description))

    async_add_entities(entities)


class GobzighBinarySensor(CoordinatorEntity[GobzighDataUpdateCoordinator], BinarySensorEntity):
    """Representation of a GOBZIGH binary sensor."""

    def __init__(
        self,
        coordinator: GobzighDataUpdateCoordinator,
        device_id: str,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device_id = device_id
        self._attr_unique_id = f"{device_id}_{description.key}"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        device_data = self.coordinator.data.get(self._device_id, {})
        return get_device_info(device_data)

    @property
    def name(self) -> str:
        """Return the name of the binary sensor."""
        device_data = self.coordinator.data.get(self._device_id, {})
        device_name = device_data.get("name", "Unknown Device")
        return f"{device_name} {self.entity_description.name}"

    @property
    def is_on(self) -> bool | None:
        """Return the state of the binary sensor."""
        device_data = self.coordinator.data.get(self._device_id, {})
        if not device_data:
            return None

        key = self.entity_description.key

        if key in ["connection_status", "is_updating"]:
            return device_data.get(key, False)
        elif key in ["has_relay", "is_auto"]:
            settings = device_data.get("settings", {})
            return settings.get(key, False)

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        device_data = self.coordinator.data.get(self._device_id, {})
        
        # For connection status, add last connected time
        if self.entity_description.key == "connection_status":
            connected_time = device_data.get("connected")
            if connected_time:
                try:
                    last_connected = dt_util.parse_datetime(connected_time)
                    return {
                        "last_connected": last_connected,
                        "time_since_last_change": self._get_time_since_last_change(last_connected)
                    }
                except (ValueError, TypeError):
                    pass
                    
        return None

    def _get_time_since_last_change(self, last_changed: datetime) -> str:
        """Get human readable time since last change."""
        if not last_changed:
            return "Unknown"
            
        now = dt_util.utcnow()
        diff = now - last_changed
        
        if diff.days > 6:
            return "More than a week ago"
        elif diff.days >= 1:
            return last_changed.strftime('%A at %H:%M')
        else:
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60
            
            if hours > 0:
                return f"{hours} hours ago"
            elif minutes > 0:
                return f"{minutes} minutes ago"
            else:
                return "Just now"
