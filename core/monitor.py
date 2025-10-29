import screen_brightness_control as sbc


def list_monitors():
    """Return a list of available monitors."""
    try:
        return sbc.list_monitors()
    except Exception:
        return []


def get_brightness(monitor_name):
    """Get current brightness of a monitor."""
    try:
        return sbc.get_brightness(display=monitor_name)[0]
    except Exception:
        return 50


def set_brightness(monitor_name, value):
    """Set brightness of a monitor."""
    try:
        sbc.set_brightness(value, display=monitor_name)
    except Exception as e:
        print(f"[Error] Setting brightness: {e}")
