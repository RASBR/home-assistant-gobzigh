"""HTTP endpoints for the GOBZIGH integration.

This exposes read-only static assets (PNG icons) under
    /api/gobzigh/static/<filename>

Used by entity_picture URLs returned from icons.py.
"""
from __future__ import annotations

import asyncio
import logging
import mimetypes
from pathlib import Path
from typing import Optional

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class GobzighStaticView(HomeAssistantView):
    """Serve static files bundled with the integration."""

    url = f"/api/{DOMAIN}/static/{{filename}}"
    name = f"api:{DOMAIN}:static"
    requires_auth = False

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        # Resolve the static directory next to this file
        self._static_dir = Path(__file__).parent / "static"

    async def get(self, request: web.Request, filename: str) -> web.StreamResponse:  # type: ignore[override]
        """Serve static files with proper path handling and logging."""
        _LOGGER.debug("Serving static file: %s", filename)
        
        # Prevent path traversal by resolving and checking the path is within static dir
        try:
            file_path = (self._static_dir / filename).resolve()
            # Ensure the resolved path is still within our static directory
            static_dir_resolved = self._static_dir.resolve()
            if not str(file_path).startswith(str(static_dir_resolved)):
                _LOGGER.warning("Path traversal attempt blocked: %s", filename)
                return web.Response(status=404, text="Not Found")
        except (ValueError, OSError) as e:
            _LOGGER.warning("Invalid path requested: %s - %s", filename, str(e))
            return web.Response(status=404, text="Not Found")

        if not file_path.exists() or not file_path.is_file():
            _LOGGER.warning("Static file not found: %s (resolved to: %s)", filename, file_path)
            return web.Response(status=404, text="Not Found")

        _LOGGER.debug("Serving file: %s (size: %d bytes)", file_path, file_path.stat().st_size)

        # Best-effort content-type
        ctype: Optional[str]
        ctype, _ = mimetypes.guess_type(file_path.name)
        if ctype is None:
            # Default to PNG since we only ship images here
            ctype = "image/png"

        # Use a FileResponse for efficient async file sending
        try:
            response = web.FileResponse(path=str(file_path), headers={"Content-Type": ctype})
            _LOGGER.debug("Successfully serving file: %s", filename)
            return response
        except Exception as e:
            _LOGGER.warning("FileResponse failed for %s: %s, trying fallback", filename, str(e))
            # Fallback to manual read (small files only)
            try:
                data = await asyncio.to_thread(file_path.read_bytes)
                _LOGGER.debug("Fallback serving successful for: %s", filename)
                return web.Response(body=data, content_type=ctype)
            except Exception as fallback_e:
                _LOGGER.error("Failed to serve file %s: %s", filename, str(fallback_e))
                return web.Response(status=500, text="Internal Server Error")


def register_http_views(hass: HomeAssistant) -> None:
    """Register HTTP views used by the integration."""
    _LOGGER.debug("Registering GOBZIGH HTTP static file server")
    hass.http.register_view(GobzighStaticView(hass))
    _LOGGER.info("GOBZIGH static file server registered at /api/%s/static/", DOMAIN)
