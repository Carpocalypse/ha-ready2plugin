
"""API client for ready2plugin."""

from __future__ import annotations

from typing import Any

from aiohttp import BasicAuth, ClientResponseError

from homeassistant.helpers.aiohttp_client import async_get_clientsession


class Ready2PluginApi:
    """Client for the local ready2plugin API."""

    def __init__(self, hass, host: str, password: str) -> None:
        self._host = host
        self._session = async_get_clientsession(hass)
        self._auth = BasicAuth("", password)

    async def get_stats(self) -> dict[str, Any]:
        """Read the statistics endpoint."""

        async with self._session.get(
            f"http://{self._host}/api/stats/__all__",
            auth=self._auth,
            timeout=10,
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def validate(self) -> str:
        """Validate connection and return serial number."""

        data = await self.get_stats()

        if "sernum" not in data:
            raise ClientResponseError(
                request_info=None,
                history=(),
                status=500,
                message="Missing serial number",
            )

        return data["sernum"]