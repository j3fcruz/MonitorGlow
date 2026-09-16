from core.monitor import ScreenBrightnessBackend


def test_list_displays(monkeypatch):
    monkeypatch.setattr("core.monitor.sbc.list_monitors", lambda: ["Panel A", "Panel B"])
    displays = ScreenBrightnessBackend().list_displays()
    assert [display.name for display in displays] == ["Panel A", "Panel B"]


def test_get_brightness(monkeypatch):
    monkeypatch.setattr("core.monitor.sbc.get_brightness", lambda display: [73])
    assert ScreenBrightnessBackend().get_brightness("Panel A") == 73


def test_set_brightness_clamps_value(monkeypatch):
    calls = []
    monkeypatch.setattr(
        "core.monitor.sbc.set_brightness",
        lambda value, display: calls.append((value, display)),
    )
    ScreenBrightnessBackend().set_brightness("Panel A", 150)
    assert calls == [(100, "Panel A")]
