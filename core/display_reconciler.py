"""Display topology reconciliation for hot-plug detection."""

from __future__ import annotations

from dataclasses import dataclass

from core.display_backend import DisplayBackend, DisplayInfo


@dataclass(frozen=True, slots=True)
class DisplayTopologyChange:
    """Difference between the previous and current display topology."""

    current: tuple[DisplayInfo, ...]
    added: tuple[DisplayInfo, ...]
    removed: tuple[DisplayInfo, ...]


class DisplayReconciler:
    """Track display identities and report additions/removals."""

    def __init__(self, backend: DisplayBackend) -> None:
        self.backend = backend
        self._known: dict[str, DisplayInfo] = {}

    def reconcile(self) -> DisplayTopologyChange:
        current = self.backend.list_displays()
        current_by_id = {display.id: display for display in current}
        added = tuple(
            display for display in current if display.id not in self._known
        )
        removed = tuple(
            display
            for display_id, display in self._known.items()
            if display_id not in current_by_id
        )
        self._known = current_by_id
        return DisplayTopologyChange(
            current=tuple(current),
            added=added,
            removed=removed,
        )
