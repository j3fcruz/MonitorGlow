import json

import pytest

from core.display_backend import DisplayInfo
from core.display_profiles import (
    DisplayProfile,
    DisplayProfileEntry,
    DisplayProfileStore,
)
from core.fake_display_backend import FakeDisplayBackend
from core.profile_service import DisplayProfileService


def test_profile_entry_validates_brightness():
    with pytest.raises(ValueError, match="between 0 and 100"):
        DisplayProfileEntry(display_id="monitor-1", brightness=101)


def test_profile_rejects_duplicate_display_ids():
    entry = DisplayProfileEntry(display_id="monitor-1", brightness=50)
    with pytest.raises(ValueError, match="duplicate"):
        DisplayProfile(name="Work", displays=(entry, entry))


def test_profile_store_round_trip(tmp_path):
    path = tmp_path / "profiles.json"
    store = DisplayProfileStore(path)
    profile = DisplayProfile(
        name="Focus",
        displays=(DisplayProfileEntry(display_id="monitor-1", brightness=35),),
    )

    store.save({profile.name: profile})

    assert store.load() == {"Focus": profile}
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1


def test_profile_service_captures_current_brightness():
    backend = FakeDisplayBackend([DisplayInfo(id="monitor-1", name="Primary")])
    backend.set_brightness("monitor-1", 42)

    profile = DisplayProfileService(backend).capture("Coding")

    assert profile.displays == (
        DisplayProfileEntry(display_id="monitor-1", brightness=42),
    )


def test_profile_service_applies_connected_and_reports_missing():
    backend = FakeDisplayBackend([DisplayInfo(id="monitor-1", name="Primary")])
    profile = DisplayProfile(
        name="Evening",
        displays=(
            DisplayProfileEntry(display_id="monitor-1", brightness=25),
            DisplayProfileEntry(display_id="monitor-2", brightness=30),
        ),
    )

    result = DisplayProfileService(backend).apply(profile)

    assert backend.get_brightness("monitor-1") == 25
    assert result.applied == ("monitor-1",)
    assert result.unavailable == ("monitor-2",)
    assert result.failed == ()
