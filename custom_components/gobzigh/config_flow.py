"""Config flow for GOBZIGH integration."""
from __future__ import annotations

import logging
import re
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .api import GobzighAPI
from .const import (
    DOMAIN,
    CONF_USER_ID,
    ERROR_NO_DEVICES,
    ERROR_INVALID_USER_ID,
    ERROR_CONNECTION,
    DEVICE_TYPES,
)

_LOGGER = logging.getLogger(__name__)

USER_SCHEMA = vol.Schema({
    vol.Required(CONF_USER_ID): cv.string,
})


def validate_user_id(user_id: str) -> bool:
    """Validate user ID format (24 character hex string)."""
    return bool(re.match(r"^[a-fA-F0-9]{24}$", user_id))


class GobzighConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for GOBZIGH."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._discovered_devices: list[dict[str, Any]] = []
        self._user_id: str = ""
        self._api: GobzighAPI | None = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return GobzighOptionsFlow(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            user_id = user_input[CONF_USER_ID].strip()
            
            # Validate user ID format
            if not validate_user_id(user_id):
                errors[CONF_USER_ID] = "invalid_user_id"
            else:
                # Test connection
                api = GobzighAPI(user_id)
                try:
                    devices = await api.async_get_devices()
                    await api.async_close()
                    
                    if devices is None:
                        errors["base"] = "cannot_connect"
                    elif len(devices) == 0:
                        # No devices found - still create the integration
                        await self.async_set_unique_id(user_id)
                        self._abort_if_unique_id_configured()
                        
                        return self.async_create_entry(
                            title=f"GOBZIGH ({user_id[:8]}...)",
                            data={CONF_USER_ID: user_id},
                            description_placeholders={"message": ERROR_NO_DEVICES}
                        )
                    else:
                        # Devices found - proceed to device selection
                        self._user_id = user_id
                        self._discovered_devices = devices
                        self._api = GobzighAPI(user_id)
                        
                        await self.async_set_unique_id(user_id)
                        self._abort_if_unique_id_configured()
                        
                        return await self.async_step_device_selection()
                        
                except Exception:
                    _LOGGER.exception("Unexpected exception")
                    errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=USER_SCHEMA,
            errors=errors,
            description_placeholders={
                "example_user_id": "507f1f77bcf86cd799439011"
            }
        )

    async def async_step_device_selection(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle device selection step."""
        if user_input is not None:
            # Create the config entry with the user ID
            return self.async_create_entry(
                title=f"GOBZIGH ({self._user_id[:8]}...)",
                data={CONF_USER_ID: self._user_id},
            )

        # Show discovered devices
        device_info = []
        for device in self._discovered_devices:
            device_type = next(
                (dt for dt in DEVICE_TYPES if dt["device_type_code"] == device.get("model_name")),
                {"type_info": {"device_type_name": "Unknown"}, "docs_url": ""}
            )
            
            device_info.append({
                "name": device.get("name", "Unknown Device"),
                "model": device.get("model_name", "Unknown"),
                "device_id": device.get("device_id", ""),
                "type_name": device_type["type_info"]["device_type_name"],
                "docs_url": device_type.get("docs_url", ""),
                "connection_status": device.get("connection_status", False),
            })

        return self.async_show_form(
            step_id="device_selection",
            data_schema=vol.Schema({}),
            description_placeholders={
                "device_count": str(len(self._discovered_devices)),
                "devices": device_info
            }
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reconfiguration."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        if not entry:
            return self.async_abort(reason="reconfigure_failed")

        if user_input is not None:
            user_id = user_input[CONF_USER_ID].strip()
            
            if not validate_user_id(user_id):
                return self.async_show_form(
                    step_id="reconfigure",
                    data_schema=USER_SCHEMA,
                    errors={CONF_USER_ID: "invalid_user_id"}
                )

            # Update the config entry
            self.hass.config_entries.async_update_entry(
                entry, data={**entry.data, CONF_USER_ID: user_id}
            )
            
            # Reload the integration
            await self.hass.config_entries.async_reload(entry.entry_id)
            
            return self.async_abort(reason="reconfigure_successful")

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema({
                vol.Required(CONF_USER_ID, default=entry.data.get(CONF_USER_ID, "")): cv.string,
            })
        )


class GobzighOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for GOBZIGH."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "scan_interval",
                    default=self.config_entry.options.get("scan_interval", 300)
                ): vol.All(vol.Coerce(int), vol.Range(min=60, max=3600))
            })
        )
