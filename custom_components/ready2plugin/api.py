"""API client for ready2plugin."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from aiohttp import BasicAuth, ClientError, ClientResponseError

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .exceptions import CannotConnect, InvalidAuth, InvalidResponse

_LOGGER = logging.getLogger(__name__)

API_TIMEOUT = 10


class Ready2PluginApi:
    """HTTP client for the ready2plugin Stromwächter."""

    def __init__(
        self,
        hass,
        host: str,
        password: str,
    ) -> None:
        """Initialize the API."""

        self._host = host
        self._password = password

        self._session = async_get_clientsession(hass)

        self._base_url = f"http://{host}"

    async def _request(
        self,
        path: str,
    ) -> dict[str, Any]:
        """Perform a GET request."""

        url = f"{self._base_url}{path}"

        _LOGGER.debug("GET %s", url)

        try:

            async with asyncio.timeout(API_TIMEOUT):

                response = await self._session.get(
                    url,
                    auth=BasicAuth(
                        login="admin",
                        password=self._password,
                    ),
                )

        except TimeoutError as err:
            raise CannotConnect from err

        except ClientError as err:
            raise CannotConnect from err

        if response.status in (401, 403):
            raise InvalidAuth

        try:
            response.raise_for_status()

        except ClientResponseError as err:
            raise CannotConnect from err

        try:
            data = await response.json()

        except Exception as err:
            raise InvalidResponse from err

        if not isinstance(data, dict):
            raise InvalidResponse

        return data
    async def async_get_stats(self) -> dict[str, Any]:
        """Return the complete statistics JSON."""

        data = await self._request("/api/stats/__all__")

        if "sernum" not in data:
            raise InvalidResponse("Missing serial number")

        if "grid_phases" not in data:
            raise InvalidResponse("Missing grid_phases")

        return data

    async def async_test_connection(self) -> str:
        """Validate the connection and return the serial number."""

        data = await self.async_get_stats()

        serial = str(data["sernum"])

        firmware = data.get("version_verstr", "unknown")

        _LOGGER.info(
            "Connected to ready2plugin %s (Firmware %s)",
            serial,
            firmware,
        )

        return serial

    async def async_get_device_info(self) -> dict[str, Any]:
        """Return basic device information."""

        data = await self.async_get_stats()

        return {
            "serial": data.get("sernum"),
            "firmware": data.get("version_verstr"),
            "build": data.get("version_buildnr"),
            "wifi_rssi": data.get("wifi_rssi"),
            "uptime": data.get("uptime"),
            "temperature": data.get("temp_mcu_esp32"),
            "wire_temperature": data.get("temp_wire"),
            "mqtt": data.get("mqtt_state"),
        }

    async def async_get_firmware(self) -> str:
        """Return the firmware version."""

        data = await self.async_get_stats()

        return str(data.get("version_verstr", ""))

    async def async_get_serial(self) -> str:
        """Return the device serial number."""

        data = await self.async_get_stats()

        return str(data["sernum"])
