"""Gobzigh coordinator for managing API communication."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any, Dict, List

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers import discovery_flow

from .const import (
    CONF_USER_ID,
    DEFAULT_SCAN_INTERVAL,
    DEVICE_DETAIL_URL,
    DEVICE_TYPES,
    DOMAIN,
    USER_DEVICE_LIST_URL,
)

_LOGGER = logging.getLogger(__name__)


class GobzighCoordinator(DataUpdateCoordinator):
    """Gobzigh data coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        # Handle both main entry (has user_id) and device entries (has device_id)
        self.user_id = entry.data.get(CONF_USER_ID)
        self.device_id = entry.data.get("device_id")
        self._session: aiohttp.ClientSession | None = None
        self._discovered_devices: Dict[str, Dict[str, Any]] = {}
        self._added_devices: set[str] = set()
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from Gobzigh API."""
        if not self._session:
            self._session = aiohttp.ClientSession()
        
        try:
            device_data = {}
            
            # If this is a device-specific coordinator, only fetch that device's data
            if self.device_id:
                detail_data = await self._fetch_device_detail(self.device_id)
                if detail_data:
                    device_data[self.device_id] = detail_data[0]  # API returns list
                return {"device_data": device_data}
            
            # If this is the main coordinator with user_id, get user devices
            if self.user_id:
                user_devices = await self._fetch_user_devices()
                
                # Get detailed data for added devices
                for device_id in self._added_devices:
                    try:
                        detail_data = await self._fetch_device_detail(device_id)
                        if detail_data:
                            device_data[device_id] = detail_data[0]  # API returns list
                    except Exception as err:
                        _LOGGER.warning(
                            "Failed to fetch device %s data: %s", device_id, err
                        )
                
                return {
                    "user_devices": user_devices,
                    "device_data": device_data,
                }
            
            return {"device_data": {}}
            
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Gobzigh API: {err}") from err

    async def _fetch_user_devices(self) -> List[Dict[str, Any]]:
        """Fetch all devices for the user."""
        if not self.user_id:
            return []
            
        url = f"{USER_DEVICE_LIST_URL}{self.user_id}"
        
        try:
            async with self._session.get(url, timeout=30) as response:
                response.raise_for_status()
                data = await response.json()
                return data if isinstance(data, list) else []
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching user devices: %s", err)
            return []

    async def _fetch_device_detail(self, device_id: str) -> List[Dict[str, Any]] | None:
        """Fetch detailed data for a specific device."""
        url = f"{DEVICE_DETAIL_URL}{device_id}"
        
        try:
            async with self._session.get(url, timeout=30) as response:
                response.raise_for_status()
                data = await response.json()
                return data if isinstance(data, list) else []
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching device %s detail: %s", device_id, err)
            return None

    async def async_start_discovery(self) -> None:
        """Start the device discovery process."""
        await self._async_discover_devices()

    async def _async_discover_devices(self) -> None:
        """Discover new devices and create discovery flows."""
        if not self.data or "user_devices" not in self.data:
            return

        user_devices = self.data["user_devices"]
        
        for device in user_devices:
            device_id = device.get("device_id")
            if not device_id:
                continue
                
            # Skip already discovered devices
            if device_id in self._discovered_devices:
                continue
                
            # Add to discovered devices
            self._discovered_devices[device_id] = device
            
            # Create discovery flow
            discovery_flow.async_create_flow(
                self.hass,
                DOMAIN,
                context={"source": "discovery"},
                data={
                    "device_id": device_id,
                    "device_data": device,
                    "user_id": self.user_id,
                },
            )
            
            _LOGGER.info("Discovered Gobzigh device: %s (%s)", 
                        device.get("name", "Unknown"), device_id)

    async def async_add_device(self, device_id: str) -> None:
        """Add a device to be monitored."""
        self._added_devices.add(device_id)
        await self.async_request_refresh()

    async def async_remove_device(self, device_id: str) -> None:
        """Remove a device from monitoring."""
        self._added_devices.discard(device_id)

    def get_device_type_info(self, model_name: str) -> Dict[str, Any] | None:
        """Get device type information from model name."""
        for device_type in DEVICE_TYPES:
            if device_type["device_type_code"] == model_name:
                return device_type
        return None

    def get_discovered_device(self, device_id: str) -> Dict[str, Any] | None:
        """Get discovered device data."""
        return self._discovered_devices.get(device_id)

    async def async_shutdown(self) -> None:
        """Shutdown coordinator and cleanup resources."""
        if self._session:
            await self._session.close()
            self._session = None
