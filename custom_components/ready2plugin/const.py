"""Constants for the ready2plugin integration."""

from datetime import timedelta

DOMAIN = "ready2plugin"

MANUFACTURER = "indielux"
MODEL = "ready2plugin Stromwächter"

DEFAULT_SCAN_INTERVAL = timedelta(seconds=5)

API_STATS = "/api/stats/__all__"

CONF_HOST = "host"
CONF_PASSWORD = "password"
