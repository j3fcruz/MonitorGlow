<div align="center">

<img src="assets/icons/icon.ico" alt="MonitorGlow Brightness Controller" width="96" height="96"/>

# MonitorGlow — Multi-Monitor Brightness Controller

**v1.0.0** · Built by [PatronHubDevs Technologies](https://www.patronhubdevs.com) · 🇵🇭 Philippines

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#-license)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![PyQt5](https://img.shields.io/badge/UI-PyQt5-41CD52?logo=qt)](https://riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows)](https://github.com/j3fcruz/MonitorGlow)
[![Offline](https://img.shields.io/badge/Offline-First-success)](#-privacy)
[![Ko-fi](https://img.shields.io/badge/Donate-Ko--fi-orange)](https://ko-fi.com/marcopolo55681)

> **Advanced Brightness & Screen Manager.**  
> Intelligent multi-monitor brightness control with system tray integration, global hotkeys, and schedule automation — offline-first, zero telemetry, zero bloat.

[Download](#-installation) · [Screenshots](#-screenshots) · [Modules](#-modules-overview) · [Contributing](#-contributing)

---

</div>

## Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dependencies](#-dependencies)
- [Modules Overview](#-modules-overview)
- [Contributing](#-contributing)
- [Privacy](#-privacy)
- [License](#-license)
- [Author](#-author)
- [Support](#-support)

---

## Overview

**MonitorGlow** is a lightweight, modular multi-monitor brightness controller built with **PyQt5**, designed for power users who need precise display control without bloatware. Adjust brightness per display, set hotkeys, automate brightness curves by time of day, and manage everything from the system tray — all without an internet connection.

Engineered with a clean layered architecture: UI / Core / Dialogs / Config — built to scale and easy to extend.

---

## Features

### Multi-Monitor Control
- Per-display brightness adjustment via intuitive slider
- Supports both internal and external monitors simultaneously
- Compatible with multi-monitor desktop setups

### System Integration
- System tray integration with single-click access
- Auto-start on Windows login (optional, via settings)
- Global keyboard shortcuts for rapid brightness adjustment

### Automation
- Automatic brightness adjustment by time-of-day schedule
- Schedule presets for day, evening, and night profiles

### Donation System
- Optional encrypted QR code donation panel
- Supports Maya, PayPal, Ko-fi, and cryptocurrency

### Offline First
- Zero network calls during normal operation
- No telemetry, no analytics, no background services

---

## Screenshots

| Welcome | Main Controller |
|---------|----------------|
| ![Welcome UI](assets/screenshots/welcome_ui.png) | ![Main UI](assets/screenshots/main_ui.png) |

| About | Help |
|-------|------|
| ![About Dialog](assets/screenshots/about_ui.png) | ![Help Dialog](assets/screenshots/help_ui.png) |

| Donate |
|--------|
| ![Donate Dialog](assets/screenshots/donate_ui.png) |

---

## Project Structure

```
MonitorGlow/
├── main.py                    # Entry point — QApplication bootstrap
├── monitor_glow.py            # Main UI and core application logic
├── requirements.txt
├── resources_rc.py            # Compiled Qt resource file (icons, QR assets)
├── .env                       # Environment variables (API keys, secrets)
│
├── config/
│   └── app_config.py          # Constants: APP_NAME, VERSION, links, QR keys
│
├── core/
│   ├── crypto_utils.py        # Encryption/decryption for secure QR donations
│   ├── monitor.py             # Monitor detection and brightness control logic
│   └── utils.py               # Helpers: notifications, registry, auto-start
│
├── dialogs/
│   ├── About_Dialog.py        # About dialog — app info and credits
│   ├── Donate_Dialog.py       # Donate dialog — QR codes, PayPal, Ko-fi, crypto
│   └── Help_Dialog.py         # Help dialog — usage instructions and tips
│
└── assets/
    └── screenshots/           # UI preview screenshots
        ├── welcome_ui.png
        ├── main_ui.png
        ├── about_ui.png
        ├── donate_ui.png
        └── help_ui.png
```

---

## Installation

### Option 1 — Prebuilt Binary (Recommended)

1. Download the latest release from [Ko-fi](https://ko-fi.com/post/Introducing-MonitorGlow-A-Sleek-Brightness-Co-W7W51IJ6S3) or [GitHub Releases](https://github.com/j3fcruz/MonitorGlow/releases)
2. Extract the ZIP archive
3. Run `MonitorGlow.exe`

> No Python installation required. Ships as a standalone executable.

### Option 2 — Run from Source

**Requirements:** Python 3.10+, Windows 10/11 (x64)

```bash
# 1. Clone the repository
git clone https://github.com/j3fcruz/MonitorGlow.git
cd MonitorGlow

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python main.py
```

---

## Usage

- Launch the app — it starts minimized in the **system tray**
- Click the tray icon to open the **brightness controller**
- Use the slider to adjust brightness per monitor
- Enable **auto-start on login** via the settings menu
- Access **About**, **Help**, or **Donate** dialogs from the tray context menu

---

## Dependencies

```
PyQt5>=5.15.7
screen_brightness_control>=1.2.0
cryptography>=41.0.0
qrcode>=7.4.2
```

```bash
pip install -r requirements.txt
```

> Brightness control relies on `screen_brightness_control` — ensure the app is run with appropriate display permissions on your system.

---

## Modules Overview

| Module | Description |
|--------|-------------|
| `main.py` | Entry point — launches the MonitorGlow application |
| `monitor_glow.py` | Main UI, core logic, and system tray integration |
| `core/monitor.py` | Monitor detection and per-display brightness control |
| `core/crypto_utils.py` | Encryption/decryption for secure QR donation payloads |
| `core/utils.py` | Helpers: notifications, Windows registry, auto-start |
| `config/app_config.py` | App constants, links, QR keys, and configuration |
| `dialogs/About_Dialog.py` | About window — app info and credits |
| `dialogs/Donate_Dialog.py` | Donate window — QR codes, PayPal, Ko-fi, crypto |
| `dialogs/Help_Dialog.py` | Help window — usage instructions and tips |
| `resources_rc.py` | Compiled Qt resources — icons and QR assets |

---

## Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Make your changes
4. Commit: `git commit -m 'Add YourFeature'`
5. Push: `git push origin feature/YourFeature`
6. Submit a Pull Request

---

## Privacy

MonitorGlow is built with a privacy-first architecture:

- **No telemetry** — zero usage data collected
- **No tracking** — no analytics, crash reporters, or fingerprinting
- **No internet required** — brightness control operates fully offline
- **QR donation system** is opt-in and self-contained — no data is transmitted automatically

---

## License

**MonitorGlow** is licensed under the **MIT License**.  
Copyright © 2025 PatronHubDevs Technologies. All rights reserved.

See [LICENSE](LICENSE) for full terms.

---

## Author

**Marco Polo**  
PatronHubDevs Technologies  
🇵🇭 Philippines  
[Website](https://www.patronhubdevs.com) · [GitHub](https://github.com/j3fcruz) · [Ko-fi](https://ko-fi.com/marcopolo55681)

---

## Support

If MonitorGlow has improved your workflow, consider supporting development:

- ⭐ **Star** the repository
- 📢 **Share** it with your network
- ☕ **[Ko-fi](https://ko-fi.com/marcopolo55681)** · 💸 **[PayPal](https://paypal.me/jofreydelacruz13)**
- 🪙 **Crypto:** BTC `1BcWJT8gBdZSPwS8UY39X9u4Afu1nZSzqk` · ETH `0xcd5eef32ff4854e4cefa13cb308b727433505bf4`

---

<div align="center">

**MonitorGlow** · PatronHubDevs Technologies · Philippines  
*Advanced Brightness & Screen Manager.*

</div>
