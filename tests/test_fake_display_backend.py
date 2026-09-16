import pytest

from core.display_backend import DisplayUnavailableError
from core.fake_display_backend import FakeDisplayBackend


def test_fake_backend_round_trip_and_clamping():
    backend = FakeDisplayBackend()
    display = backend.list_displays()[0]

    backend.set_brightness(display.id, 77)
    assert backend.get_brightness(display.id) == 77

    backend.set_brightness(display.id, -5)
    assert backend.get_brightness(display.id) == 0

    backend.set_brightness(display.id, 500)
    assert backend.get_brightness(display.id) == 100


def test_fake_backend_rejects_missing_display():
    backend = FakeDisplayBackend()
    with pytest.raises(DisplayUnavailableError):
        backend.get_brightness("missing")
