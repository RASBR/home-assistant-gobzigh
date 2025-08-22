"""API client for GOBZIGH integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import async_timeout

from .const import USER_DEVICE_LIST_URL, DEVICE_URL

_LOGGER = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds


class GobzighAPIError(Exception):
    """Base exception for GOBZIGH API errors."""


class GobzighConnectionError(GobzighAPIError):
    """Connection error."""


class GobzighAuthError(GobzighAPIError):
    """Authentication error."""


class GobzighAPI:
    """GOBZIGH API client."""

    def __init__(self, user_id: str) -> None:
        """Initialize the API client."""
        self.user_id = user_id
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get aiohttp session."""
        if self._session is None:
            timeout = aiohttp.ClientTimeout(total=30)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def async_close(self) -> None:
        """Close the session."""
        if self._session:
            await self._session.close()
            self._session = None

    async def _make_request(self, url: str) -> dict[str, Any] | list[dict[str, Any]] | None:
        """Make HTTP request with retry logic."""
        for attempt in range(MAX_RETRIES):
            try:
                session = await self._get_session()
                async with async_timeout.timeout(30):
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data
                        elif response.status == 401:
                            raise GobzighAuthError("Invalid user ID or unauthorized")
                        elif response.status == 404:
                            _LOGGER.warning("API endpoint not found: %s", url)
                            return None
                        else:
                            _LOGGER.error("API request failed with status %s", response.status)
                            raise GobzighConnectionError(f"HTTP {response.status}")
                            
            except asyncio.TimeoutError:
                _LOGGER.warning("Timeout on attempt %d/%d", attempt + 1, MAX_RETRIES)
                if attempt == MAX_RETRIES - 1:
                    raise GobzighConnectionError("Request timeout")
                    
            except aiohttp.ClientError as err:
                _LOGGER.warning("Client error on attempt %d/%d: %s", attempt + 1, MAX_RETRIES, err)
                if attempt == MAX_RETRIES - 1:
                    raise GobzighConnectionError(f"Connection error: {err}")
                    
            except Exception as err:
                _LOGGER.error("Unexpected error: %s", err)
                raise GobzighAPIError(f"Unexpected error: {err}")
                
            # Wait before retry
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                
        return None

    async def async_get_devices(self) -> list[dict[str, Any]] | None:
        """Get all devices for the user."""
        url = f"{USER_DEVICE_LIST_URL}?user_id={self.user_id}"
        
        try:
            data = await self._make_request(url)
            if isinstance(data, list):
                return data
            else:
                _LOGGER.error("Invalid response format: expected list, got %s", type(data))
                return None
        except GobzighAPIError:
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error getting devices: %s", err)
            return None

    async def async_get_device_data(self, device_id: str) -> dict[str, Any] | None:
        """Get data for a specific device."""
        url = f"{DEVICE_URL}?device_id={device_id}"
        
        try:
            data = await self._make_request(url)
            if isinstance(data, list) and len(data) > 0:
                return data[0]  # Return the first device
            else:
                _LOGGER.warning("No data returned for device %s", device_id)
                return None
        except GobzighAPIError:
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error getting device %s data: %s", device_id, err)
            return None

    async def async_control_relay(self, device_id: str, state: bool) -> bool:
        """Control device relay state."""
        # This would need to be implemented based on the actual API endpoint
        # For now, we'll return True as a placeholder
        _LOGGER.warning("Relay control not yet implemented for device %s", device_id)
        return True
