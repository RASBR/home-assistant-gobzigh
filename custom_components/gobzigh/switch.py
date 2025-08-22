"""Switch platform for GOBZIGH integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import get_device_info
from .const import DOMAIN
from .coordinator import GobzighDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

SWITCH_DESCRIPTIONS: tuple[SwitchEntityDescription, ...] = (
    SwitchEntityDescription(
        key="relay_state",
        name="Relay",
        icon="mdi:electric-switch",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up GOBZIGH switches from a config entry."""
    coordinator: GobzighDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for device_id, device_data in coordinator.data.items():
        # Only create switches for devices that have a relay
        settings = device_data.get("settings", {})
        if settings.get("has_relay", False):
            for description in SWITCH_DESCRIPTIONS:
                entities.append(GobzighSwitch(coordinator, device_id, description))

    async_add_entities(entities)


class GobzighSwitch(CoordinatorEntity[GobzighDataUpdateCoordinator], SwitchEntity):
    """Representation of a GOBZIGH switch."""

    def __init__(
        self,
        coordinator: GobzighDataUpdateCoordinator,
        device_id: str,
        description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch."""
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
        """Return the name of the switch."""
        device_data = self.coordinator.data.get(self._device_id, {})
        device_name = device_data.get("name", "Unknown Device")
        return f"{device_name} {self.entity_description.name}"

    @property
    def is_on(self) -> bool | None:
        """Return the state of the switch."""
        device_data = self.coordinator.data.get(self._device_id, {})
        if not device_data:
            return None

        return device_data.get("relay_state", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        success = await self.coordinator.async_control_relay(self._device_id, True)
        if not success:
            _LOGGER.error("Failed to turn on relay for device %s", self._device_id)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        success = await self.coordinator.async_control_relay(self._device_id, False)
        if not success:
            _LOGGER.error("Failed to turn off relay for device %s", self._device_id)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        device_data = self.coordinator.data.get(self._device_id, {})
        settings = device_data.get("settings", {})
        
        return {
            "auto_mode": settings.get("is_auto", False),
            "open_threshold": settings.get("o_relay", 0),
            "close_threshold": settings.get("c_relay", 0),
            "power_on_state": device_data.get("power_on_state", ""),
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        device_data = self.coordinator.data.get(self._device_id, {})
        return (
            super().available and 
            device_data.get("connection_status", False) and
            not device_data.get("is_updating", False)
        )
