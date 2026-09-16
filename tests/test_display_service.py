import threading
import time

from core.display_service import DisplayCommandService
from core.fake_display_backend import FakeDisplayBackend


def test_rapid_writes_are_coalesced_to_latest_value():
    backend = FakeDisplayBackend()
    service = DisplayCommandService(backend, debounce_seconds=0.02)
    completed = threading.Event()

    service.set_brightness("display-1", 10)
    service.set_brightness("display-1", 40)
    service.set_brightness("display-1", 73, on_success=lambda _value: completed.set())

    assert completed.wait(1.0)
    assert backend.get_brightness("display-1") == 73
    service.close()


def test_values_are_clamped_before_background_write():
    backend = FakeDisplayBackend()
    service = DisplayCommandService(backend, debounce_seconds=0.01)
    completed = threading.Event()

    service.set_brightness("display-1", 999, on_success=lambda _value: completed.set())

    assert completed.wait(1.0)
    assert backend.get_brightness("display-1") == 100
    service.close()


def test_close_cancels_pending_write():
    backend = FakeDisplayBackend()
    original = backend.get_brightness("display-1")
    service = DisplayCommandService(backend, debounce_seconds=0.2)

    service.set_brightness("display-1", 12)
    service.close()
    time.sleep(0.25)

    assert backend.get_brightness("display-1") == original
