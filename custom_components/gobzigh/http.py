"""HTTP endpoints for the GOBZIGH integration.

This exposes read-only static assets (PNG icons) under
    /api/gobzigh/static/<filename>

Used by entity_picture URLs returned from icons.py.
"""
from __future__ import annotations

import asyncio
import mimetypes
from pathlib import Path
from typing import Optional

from aiohttp import web
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN


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
        # Prevent path traversal
        safe_name = Path(filename).name

        file_path = self._static_dir / safe_name
        if not file_path.exists() or not file_path.is_file():
            return web.Response(status=404, text="Not Found")

        # Best-effort content-type
        ctype: Optional[str]
        ctype, _ = mimetypes.guess_type(file_path.name)
        if ctype is None:
            # Default to PNG since we only ship images here
            ctype = "image/png"

        # Use a FileResponse for efficient async file sending
        try:
            return web.FileResponse(path=str(file_path), headers={"Content-Type": ctype})
        except Exception:
            # Fallback to manual read (small files only)
            data = await asyncio.to_thread(file_path.read_bytes)
            return web.Response(body=data, content_type=ctype)


def register_http_views(hass: HomeAssistant) -> None:
    """Register HTTP views used by the integration."""
    hass.http.register_view(GobzighStaticView(hass))
