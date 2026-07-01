"""Exceptions for the ready2plugin integration."""

from __future__ import annotations


class Ready2PluginError(Exception):
    """Base exception for ready2plugin."""


class CannotConnect(Ready2PluginError):
    """Raised when the device cannot be reached."""


class InvalidAuth(Ready2PluginError):
    """Raised when authentication fails."""


class InvalidResponse(Ready2PluginError):
    """Raised when the device returned an unexpected response."""
