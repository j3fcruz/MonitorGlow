from core.display_backend import DisplayInfo
from core.display_profiles import DisplayProfile, DisplayProfileEntry
from core.fake_display_backend import FakeDisplayBackend
from core.profile_automation import DisplayProfileRestorer


def _profile() -> DisplayProfile:
    return DisplayProfile(
        name="Coding",
        displays=(DisplayProfileEntry(display_id="monitor-1", brightness=35),),
    )


def test_restorer_does_nothing_without_active_profile():
    backend = FakeDisplayBackend([DisplayInfo(id="monitor-1", name="Primary")])
    result = DisplayProfileRestorer(backend).reconcile()
    assert result.restored == ()
    assert backend.get_brightness("monitor-1") == 50


def test_restorer_applies_profile_when_known_display_appears():
    backend = FakeDisplayBackend([])
    restorer = DisplayProfileRestorer(backend)
    restorer.set_active_profile(_profile())
    restorer.mark_current_topology()

    backend._displays = [DisplayInfo(id="monitor-1", name="Primary")]
    backend._brightness = {"monitor-1": 50}
    result = restorer.reconcile()

    assert result.restored == ("monitor-1",)
    assert backend.get_brightness("monitor-1") == 35


def test_restorer_does_not_override_manual_change_without_reconnect():
    backend = FakeDisplayBackend([DisplayInfo(id="monitor-1", name="Primary")])
    restorer = DisplayProfileRestorer(backend)
    restorer.set_active_profile(_profile())
    restorer.mark_current_topology()
    backend.set_brightness("monitor-1", 80)

    result = restorer.reconcile()

    assert result.restored == ()
    assert backend.get_brightness("monitor-1") == 80


def test_restorer_reapplies_after_disconnect_and_reconnect():
    backend = FakeDisplayBackend([DisplayInfo(id="monitor-1", name="Primary")])
    restorer = DisplayProfileRestorer(backend)
    restorer.set_active_profile(_profile())
    restorer.mark_current_topology()

    backend._displays = []
    backend._brightness = {}
    restorer.reconcile()

    backend._displays = [DisplayInfo(id="monitor-1", name="Primary")]
    backend._brightness = {"monitor-1": 60}
    result = restorer.reconcile()

    assert result.restored == ("monitor-1",)
    assert backend.get_brightness("monitor-1") == 35
