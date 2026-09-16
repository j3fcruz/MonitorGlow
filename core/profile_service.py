"""Capture and apply persistent display workspace profiles."""

from __future__ import annotations

from dataclasses import dataclass

from core.display_backend import DisplayBackend
from core.display_profiles import DisplayProfile, DisplayProfileEntry


@dataclass(frozen=True, slots=True)
class ProfileApplyResult:
    """Result of applying a profile to currently connected displays."""

    applied: tuple[str, ...]
    unavailable: tuple[str, ...]
    failed: tuple[str, ...]


class DisplayProfileService:
    """Create and apply profiles without assuming every display is connected."""

    def __init__(self, backend: DisplayBackend) -> None:
        self.backend = backend

    def capture(self, name: str) -> DisplayProfile:
        entries = tuple(
            DisplayProfileEntry(
                display_id=display.id,
                brightness=self.backend.get_brightness(display.id),
            )
            for display in self.backend.list_displays()
        )
        return DisplayProfile(name=name, displays=entries)

    def apply(self, profile: DisplayProfile) -> ProfileApplyResult:
        connected = {display.id for display in self.backend.list_displays()}
        applied: list[str] = []
        unavailable: list[str] = []
        failed: list[str] = []

        for entry in profile.displays:
            if entry.display_id not in connected:
                unavailable.append(entry.display_id)
                continue
            try:
                self.backend.set_brightness(entry.display_id, entry.brightness)
            except Exception:
                failed.append(entry.display_id)
            else:
                applied.append(entry.display_id)

        return ProfileApplyResult(
            applied=tuple(applied),
            unavailable=tuple(unavailable),
            failed=tuple(failed),
        )
