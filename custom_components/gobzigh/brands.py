"""Brand support utilities for Gobzigh integration."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any

from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class GobzighBrandManager:
    """Manage brand assets and fallbacks for Gobzigh integration."""
    
    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the brand manager."""
        self.hass = hass
        self._static_path = Path(__file__).parent
        
    def get_integration_icon_url(self) -> str | None:
        """Get the integration icon URL for frontend display."""
        # Home Assistant should try CDN first, then our fallback
        return f"/api/brands/{DOMAIN}/icon.png"
        
    def get_integration_logo_url(self) -> str | None:
        """Get the integration logo URL for frontend display."""
        # Home Assistant should try CDN first, then our fallback
        return f"/api/brands/{DOMAIN}/logo.png"
        
    def has_local_icon(self) -> bool:
        """Check if local icon exists."""
        paths_to_check = [
            self._static_path / "brands" / DOMAIN / "icon.png",
            self._static_path / "icon.png"
        ]
        return any(path.exists() for path in paths_to_check)
        
    def has_local_logo(self) -> bool:
        """Check if local logo exists."""
        paths_to_check = [
            self._static_path / "brands" / DOMAIN / "logo.png", 
            self._static_path / "logo.png"
        ]
        return any(path.exists() for path in paths_to_check)
        
    def get_device_brand_info(self, device_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get brand information for device registration."""
        # This ensures devices get proper brand info
        brand_info = {
            "manufacturer": "Gobzigh",
            "model": device_data.get("model_name", "Unknown"),
            "name": device_data.get("name", f"Gobzigh {device_data.get('model_name', 'Device')}"),
            "sw_version": device_data.get("firmware_version", "Unknown"),
        }
        
        # Add brand URLs that Home Assistant frontend can use
        if self.has_local_icon():
            brand_info["icon_url"] = f"/api/brands/{DOMAIN}/icon.png"
        if self.has_local_logo():
            brand_info["logo_url"] = f"/api/brands/{DOMAIN}/logo.png"
            
        return brand_info
