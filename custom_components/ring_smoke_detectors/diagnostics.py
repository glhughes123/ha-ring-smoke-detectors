"""Diagnostics support for Ring Smoke Detectors.

Lets you download the current device payload from the UI:
Settings -> Devices & Services -> Ring Smoke Detectors -> the three-dot
menu -> Download diagnostics. Device identifiers and location data are
redacted, so the result is safe to share when reporting an issue.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from .const import CONF_REFRESH_TOKEN
from .coordinator import RingSmokeConfigEntry

# Keys whose values are redacted anywhere they appear in the payload.
TO_REDACT = {
    CONF_REFRESH_TOKEN,
    "serialNumber",
    "zid",
    "location_id",
    "latitude",
    "longitude",
    "address",
    "email",
    "ssid",
    "macAddress",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: RingSmokeConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    devices = [
        {
            "available": coordinator.is_device_available(zid),
            "data": async_redact_data(data, TO_REDACT),
        }
        for zid, data in coordinator.devices.items()
    ]

    return {
        "entry_data": async_redact_data(dict(entry.data), TO_REDACT),
        "entry_options": dict(entry.options),
        "device_count": len(coordinator.devices),
        "devices": devices,
    }
