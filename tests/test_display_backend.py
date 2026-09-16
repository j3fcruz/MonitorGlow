import pytest

from core.display_backend import DisplayInfo


def test_display_info_is_immutable():
    display = DisplayInfo(id="display-1", name="Primary")
    assert display.id == "display-1"
    assert display.name == "Primary"
    with pytest.raises(Exception):
        display.name = "Changed"
