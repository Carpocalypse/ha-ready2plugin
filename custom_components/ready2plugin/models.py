"""Data models for the ready2plugin API."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Phase:
    """Grid phase."""

    current: float
    voltage: float
    power: float
    power_factor: float


@dataclass(slots=True, frozen=True)
class Stats:
    """Current device statistics."""

    serial: str
    firmware: str
    build: int

    wifi_rssi: int

    esp_temperature: float
    wire_temperature: float

    uptime: int

    mqtt_connected: bool

    free_memory: int
    allocated_memory: int

    phases: list[Phase]

    max_feed_power: float
