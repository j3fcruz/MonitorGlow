"""Persistent workspace profiles for display settings."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DisplayProfileEntry:
    """Desired settings for one stable display identity."""

    display_id: str
    brightness: int

    def __post_init__(self) -> None:
        if not self.display_id.strip():
            raise ValueError("display_id must not be empty")
        if not 0 <= self.brightness <= 100:
            raise ValueError("brightness must be between 0 and 100")


@dataclass(frozen=True, slots=True)
class DisplayProfile:
    """Named collection of display settings."""

    name: str
    displays: tuple[DisplayProfileEntry, ...]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("profile name must not be empty")
        ids = [entry.display_id for entry in self.displays]
        if len(ids) != len(set(ids)):
            raise ValueError("profile contains duplicate display IDs")


class DisplayProfileStore:
    """JSON-backed profile store with atomic replacement."""

    SCHEMA_VERSION = 1

    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def load(self) -> dict[str, DisplayProfile]:
        if not self.path.exists():
            return {}
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != self.SCHEMA_VERSION:
            raise ValueError("unsupported display profile schema")
        profiles: dict[str, DisplayProfile] = {}
        for item in payload.get("profiles", []):
            entries = tuple(
                DisplayProfileEntry(**entry) for entry in item.get("displays", [])
            )
            profile = DisplayProfile(name=item["name"], displays=entries)
            profiles[profile.name] = profile
        return profiles

    def save(self, profiles: dict[str, DisplayProfile]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": self.SCHEMA_VERSION,
            "profiles": [
                {
                    "name": profile.name,
                    "displays": [asdict(entry) for entry in profile.displays],
                }
                for profile in sorted(profiles.values(), key=lambda item: item.name)
            ],
        }
        temporary = self.path.with_suffix(f"{self.path.suffix}.tmp")
        temporary.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.path)
