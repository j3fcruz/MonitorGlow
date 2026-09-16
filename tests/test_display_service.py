import time

import pytest

from core.display_service import DisplayCommandService
from core.fake_display_backend import FakeDisplayBackend


def test_async_reads_return_futures():
    backend = FakeDisplayBackend()
    with DisplayCommandService(backend, debounce_seconds=0) as service:
        displays = service.list_displays().result(timeout=1)
        assert displays[0].id == "fake-1"
        assert service.get_brightness("fake-1").result(timeout=1) == 50


def test_brightness_writes_are_clamped():
    backend = FakeDisplayBackend()
    with DisplayCommandService(backend, debounce_seconds=0.01) as service:
        service.set_brightness("fake-1", 500)
        time.sleep(0.05)
        assert backend.get_brightness("fake-1") == 100


def test_latest_brightness_write_wins():
    backend = FakeDisplayBackend()
    with DisplayCommandService(backend, debounce_seconds=0.04) as service:
        service.set_brightness("fake-1", 10)
        service.set_brightness("fake-1", 20)
        service.set_brightness("fake-1", 73)
        time.sleep(0.1)
        assert backend.get_brightness("fake-1") == 73


def test_service_rejects_commands_after_shutdown():
    service = DisplayCommandService(FakeDisplayBackend())
    service.shutdown()
    with pytest.raises(RuntimeError, match="shut down"):
        service.get_brightness("fake-1")
