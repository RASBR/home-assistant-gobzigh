"""HTTP views for Gobzigh integration."""
from __future__ import annotations

import logging
import mimetypes
from pathlib import Path

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class GobzighIconView(HomeAssistantView):
    """View to serve Gobzigh static files."""

    url = f"/api/{DOMAIN}/icon/{{filename}}"
    name = f"api:{DOMAIN}:icon"
    requires_auth = False

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the view."""
        self.hass = hass
        self._static_path = Path(__file__).parent

    async def get(self, request: web.Request, filename: str) -> web.Response:
        """Serve static files."""
        if filename not in ["icon.png", "logo.png"]:
            return web.Response(status=404)

        file_path = self._static_path / filename
        
        if not file_path.exists():
            _LOGGER.error("Static file not found: %s", file_path)
            return web.Response(status=404)

        try:
            content_type, _ = mimetypes.guess_type(str(file_path))
            if not content_type:
                content_type = "application/octet-stream"

            with open(file_path, "rb") as file:
                content = file.read()

            return web.Response(
                body=content,
                content_type=content_type,
                headers={"Cache-Control": "public, max-age=3600"},
            )
        except Exception as err:
            _LOGGER.error("Error serving static file %s: %s", filename, err)
            return web.Response(status=500)


async def async_setup_http_views(hass: HomeAssistant) -> None:
    """Set up HTTP views for Gobzigh."""
    hass.http.register_view(GobzighIconView(hass))
