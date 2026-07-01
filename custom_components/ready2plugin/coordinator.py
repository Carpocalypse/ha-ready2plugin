
"""DataUpdateCoordinator."""

from __future__ import annotations

import logging

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import Ready2PluginApi
from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class Ready2PluginCoordinator(DataUpdateCoordinator):
    """Coordinator."""

    def __init__(self, hass, api: Ready2PluginApi) -> None:

        super().__init__(
            hass,
            _LOGGER,
            name="ready2plugin",
            update_interval=DEFAULT_SCAN_INTERVAL,
        )

        self.api = api

    async def _async_update_data(self):

        try:
            return await self.api.get_stats()

        except Exception as err:
            raise UpdateFailed(err) from err