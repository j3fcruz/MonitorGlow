"""Default display backend using screen_brightness_control.

UI code should depend on DisplayBackend rather than importing the hardware
library directly. This keeps MonitorGlow ready for dedicated Windows, Linux,
and macOS adapters later.
"""

from __future__ import annotations

import logging

import screen_brightness_control as sbc

from core.display_backend import (
    DisplayBackend,
    DisplayInfo,
    DisplayOperationError,
    DisplayUnavailableError,
)

logger = logging.getLogger(__name__)


class ScreenBrightnessBackend(DisplayBackend):
    def list_displays(self) -> list[DisplayInfo]:
        try:
            names = sbc.list_monitors()
        except Exception as exc:
            logger.exception("Display enumeration failed")
            raise DisplayOperationError("Unable to enumerate displays") from exc
        return [DisplayInfo(id=name, name=name) for name in names]

    def get_brightness(self, display_id: str) -> int:
        try:
            values = sbc.get_brightness(display=display_id)
            if not values:
                raise DisplayUnavailableError(f"No brightness value for {display_id}")
            return max(0, min(100, int(values[0])))
        except DisplayUnavailableError:
            raise
        except Exception as exc:
            logger.exception("Brightness read failed for %s", display_id)
            raise DisplayOperationError(f"Unable to read brightness for {display_id}") from exc

    def set_brightness(self, display_id: str, value: int) -> None:
        value = max(0, min(100, int(value)))
        try:
            sbc.set_brightness(value, display=display_id)
        except Exception as exc:
            logger.exception("Brightness write failed for %s", display_id)
            raise DisplayOperationError(f"Unable to set brightness for {display_id}") from exc


_default_backend = ScreenBrightnessBackend()


def list_monitors() -> list[str]:
    """Backward-compatible monitor-name API."""
    return [display.name for display in _default_backend.list_displays()]


def get_brightness(monitor_name: str) -> int:
    return _default_backend.get_brightness(monitor_name)


def set_brightness(monitor_name: str, value: int) -> None:
    _default_backend.set_brightness(monitor_name, value)
