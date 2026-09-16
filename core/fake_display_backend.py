"""Deterministic in-memory display backend for tests and diagnostics."""

from __future__ import annotations

from core.display_backend import DisplayBackend, DisplayInfo, DisplayUnavailableError


class FakeDisplayBackend(DisplayBackend):
    """Hardware-free backend that behaves like a small display fleet."""

    def __init__(self, displays: list[DisplayInfo] | None = None) -> None:
        self._displays = displays or [DisplayInfo(id="fake-1", name="Fake Display")]
        self._brightness = {display.id: 50 for display in self._displays}

    def list_displays(self) -> list[DisplayInfo]:
        return list(self._displays)

    def get_brightness(self, display_id: str) -> int:
        self._require(display_id)
        return self._brightness[display_id]

    def set_brightness(self, display_id: str, value: int) -> None:
        self._require(display_id)
        self._brightness[display_id] = max(0, min(100, int(value)))

    def _require(self, display_id: str) -> None:
        if display_id not in self._brightness:
            raise DisplayUnavailableError(f"Display is unavailable: {display_id}")
