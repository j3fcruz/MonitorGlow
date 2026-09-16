"""Automatic restoration of display profiles after topology changes."""

from __future__ import annotations

from dataclasses import dataclass

from core.display_backend import DisplayBackend
from core.display_profiles import DisplayProfile


@dataclass(frozen=True, slots=True)
class RestoreResult:
    """Settings restored during one topology reconciliation pass."""

    restored: tuple[str, ...]
    failed: tuple[str, ...]


class DisplayProfileRestorer:
    """Restore known settings only when displays newly appear.

    The restorer deliberately avoids continuously forcing brightness. It acts
    only on newly connected display IDs, which makes manual brightness changes
    remain under user control between topology changes.
    """

    def __init__(self, backend: DisplayBackend) -> None:
        self.backend = backend
        self._known_ids: set[str] = set()
        self._active_profile: DisplayProfile | None = None

    def set_active_profile(self, profile: DisplayProfile | None) -> None:
        self._active_profile = profile

    def reconcile(self) -> RestoreResult:
        current_ids = {display.id for display in self.backend.list_displays()}
        added_ids = current_ids - self._known_ids
        self._known_ids = current_ids

        profile = self._active_profile
        if profile is None or not added_ids:
            return RestoreResult(restored=(), failed=())

        settings = {entry.display_id: entry.brightness for entry in profile.displays}
        restored: list[str] = []
        failed: list[str] = []
        for display_id in sorted(added_ids):
            if display_id not in settings:
                continue
            try:
                self.backend.set_brightness(display_id, settings[display_id])
            except Exception:
                failed.append(display_id)
            else:
                restored.append(display_id)
        return RestoreResult(restored=tuple(restored), failed=tuple(failed))

    def mark_current_topology(self) -> None:
        """Prime topology state without changing any display settings."""
        self._known_ids = {display.id for display in self.backend.list_displays()}
