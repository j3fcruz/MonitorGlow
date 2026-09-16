"""Select the safest display backend for the current operating system."""

from __future__ import annotations

import sys

from core.display_backend import DisplayBackend
from core.monitor import ScreenBrightnessBackend


def create_display_backend(platform: str | None = None) -> DisplayBackend:
    """Create the display backend for a supported desktop platform.

    screen-brightness-control currently provides the common implementation on
    Windows and Linux. macOS support is kept behind the same contract so a
    native adapter can replace it without changing presentation code.
    """
    platform = platform or sys.platform
    if platform.startswith(("win", "linux", "darwin")):
        return ScreenBrightnessBackend()
    return ScreenBrightnessBackend()
