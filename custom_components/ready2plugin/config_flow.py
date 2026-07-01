"""Config flow for ready2plugin."""

from __future__ import annotations

import logging

from aiohttp import ClientError, ClientResponseError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import callback

from .api import Ready2PluginApi
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class CannotConnect(Exception):
    """Unable to connect."""


class InvalidAuth(Exception):
    """Invalid authentication."""


async def validate_input(hass, data):
    """Validate user input."""

    api = Ready2PluginApi(
        hass,
        data[CONF_HOST],
        data[CONF_PASSWORD],
    )

    try:
        serial = await api.validate()

    except ClientResponseError as err:
        if err.status in (401, 403):
            raise InvalidAuth from err
        raise CannotConnect from err

    except ClientError as err:
        raise CannotConnect from err

    return {
        "title": f"ready2plugin ({data[CONF_HOST]})",
        "serial": serial,
    }


class Ready2PluginConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):

        errors = {}

        if user_input is not None:

            try:

                info = await validate_input(
                    self.hass,
                    user_input,
                )

            except CannotConnect:
                errors["base"] = "cannot_connect"

            except InvalidAuth:
                errors["base"] = "invalid_auth"

            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            else:

                await self.async_set_unique_id(
                    info["serial"]
                )

                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return options flow."""
        return Ready2PluginOptionsFlow(config_entry)


class Ready2PluginOptionsFlow(config_entries.OptionsFlow):
    """Options flow."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input,
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )
