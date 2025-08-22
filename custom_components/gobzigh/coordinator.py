"""Data update coordinator for GOBZIGH integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import GobzighAPI
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class GobzighDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching GOBZIGH data."""

    def __init__(self, hass: HomeAssistant, api: GobzighAPI) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api
        self.devices: dict[str, dict[str, Any]] = {}

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            devices_data = await self.api.async_get_devices()
            if devices_data is None:
                raise UpdateFailed("Failed to get devices data")

            # Store devices data indexed by device_id
            updated_devices = {}
            for device in devices_data:
                device_id = device.get("device_id")
                if device_id:
                    updated_devices[device_id] = device

            self.devices = updated_devices
            return updated_devices

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def async_get_device_data(self, device_id: str) -> dict[str, Any] | None:
        """Get specific device data."""
        return self.data.get(device_id) if self.data else None

    async def async_control_relay(self, device_id: str, state: bool) -> bool:
        """Control device relay."""
        success = await self.api.async_control_relay(device_id, state)
        if success:
            # Update the local data immediately for better UX
            if self.data and device_id in self.data:
                self.data[device_id]["relay_state"] = state
                self.async_update_listeners()
        return success
