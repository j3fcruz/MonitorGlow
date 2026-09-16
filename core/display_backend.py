"""Platform-neutral display backend contract for MonitorGlow."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class DisplayError(RuntimeError):
    """Base error raised by display backends."""


class DisplayUnavailableError(DisplayError):
    """Raised when a requested display is no longer available."""


class DisplayOperationError(DisplayError):
    """Raised when a display operation cannot be completed."""


@dataclass(frozen=True, slots=True)
class DisplayInfo:
    """Stable, UI-safe representation of a detected display."""

    id: str
    name: str


class DisplayBackend(ABC):
    """Contract implemented by OS/hardware-specific display backends."""

    @abstractmethod
    def list_displays(self) -> list[DisplayInfo]:
        raise NotImplementedError

    @abstractmethod
    def get_brightness(self, display_id: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_brightness(self, display_id: str, value: int) -> None:
        raise NotImplementedError
