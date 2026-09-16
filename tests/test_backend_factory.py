from core.backend_factory import create_display_backend
from core.monitor import ScreenBrightnessBackend


def test_factory_returns_backend_for_supported_platforms():
    for platform in ("win32", "linux", "darwin"):
        assert isinstance(create_display_backend(platform), ScreenBrightnessBackend)
