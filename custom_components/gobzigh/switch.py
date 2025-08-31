"""Gobzigh switch platform."""
from __future__ import annotations

import logging
from typing import Any, Dict

import aiohttp
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GobzighCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gobzigh switches."""
    coordinator: GobzighCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities: list[SwitchEntity] = []
    
    # Check if this is a device entry
    if "device_id" in config_entry.data:
        device_id = config_entry.data["device_id"]
        device_data = config_entry.data.get("device_data", {})
        model_name = device_data.get("model_name", "")
        device_name = device_data.get("name", "Gobzigh Device")
        
        # Create switch for devices that support relay control
        if model_name == "WLSV0":  # Liquid Level device with relay
            settings = device_data.get("settings", {})
            if settings.get("has_relay", False):
                entities.append(GobzighRelaySwitchEntity(coordinator, device_id, device_name))
    
    async_add_entities(entities)


class GobzighRelaySwitchEntity(CoordinatorEntity, SwitchEntity):
    """Gobzigh relay switch entity."""

    def __init__(
        self,
        coordinator: GobzighCoordinator,
        device_id: str,
        device_name: str,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_name = device_name
        self._attr_unique_id = f"{device_id}_switch"
        self._attr_name = f"{device_name} Switch"

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information."""
        device_data = self.coordinator.data.get("device_data", {}).get(self._device_id, {})
        model_name = device_data.get("model_name", "Unknown")
        firmware_version = device_data.get("firmware_version", "Unknown")
        
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": "Gobzigh",
            "model": model_name,
            "sw_version": firmware_version,
            "connections": {("mac", self._device_id)},
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self._device_id in self.coordinator.data.get("device_data", {})
        )

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        device_data = self.coordinator.data.get("device_data", {}).get(self._device_id, {})
        relay_state = device_data.get("relay_state")
        return relay_state if isinstance(relay_state, bool) else None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._async_set_relay_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._async_set_relay_state(False)

    async def _async_set_relay_state(self, state: bool) -> None:
        """Set the relay state."""
        url = f"https://test.gobzigh.com/v1/level-sensor-device/relay"
        
        payload = {
            "device_id": self._device_id,
            "relay_state": state
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=30) as response:
                    response.raise_for_status()
                    _LOGGER.debug("Successfully set relay state for device %s to %s", 
                                self._device_id, state)
                    
                    # Request immediate refresh to update state
                    await self.coordinator.async_request_refresh()
                    
        except aiohttp.ClientError as err:
            _LOGGER.error("Failed to set relay state for device %s: %s", 
                        self._device_id, err)
        except Exception as err:
            _LOGGER.error("Unexpected error setting relay state for device %s: %s", 
                        self._device_id, err)
