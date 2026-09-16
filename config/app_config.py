from dotenv import load_dotenv
import os
import resources_rc  # noqa: F401 - registers Qt resources

load_dotenv()

APP_NAME = "MonitorGlow"
ABOUT_APP = "A Multi-Monitor Brightness Controller"
AUTHOR = "Marco Polo"
APP_DEVELOPER = "PatronHubDevs Technologies"
APP_VERSION = "1.2.0"

APP_ICON = ":/assets/icons/icon.png"
MAYA_QR_FILE = ":/assets/resources/maya_qr.bin"

COPYRIGHT = f"© 2026 {APP_NAME}. All rights reserved."

# Optional runtime configuration. Do not treat values bundled with a desktop
# executable as secrets; client-side application material can be recovered.
MAYA_QR_KEY = os.getenv("MAYA_QR_KEY", "").encode()
PAYPAL_LINK = os.getenv("PAYPAL_LINK", "")
KOFI_LINK = os.getenv("KOFI_LINK", "")

GITHUB_LINK = "https://github.com/j3fcruz"
BTC_LINK = "1BcWJT8gBdZSPwS8UY39X9u4Afu1nZSzqk"
ETH_LINK = "0xcd5eef32ff4854e4cefa13cb308b727433505bf4"

DESCRIPTION = f"""{APP_NAME} by {AUTHOR} is a lightweight system tray utility
that allows you to control the brightness of connected displays.

Features:

• Adjust brightness for one or multiple monitors
• Supports internal and compatible external displays
• System tray integration with quick access
• Dark theme for better visibility
• Minimal, modern UI with About and Donate sections
• Offline-first display control
"""
