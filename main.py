# main.py

import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

from monitor_glow import MonitorGlow
from config.app_config import APP_NAME, APP_DEVELOPER, APP_ICON, AUTHOR
from core.utils import notification_message


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    slider = MonitorGlow()

    # ---------------------------------------------
    # System tray icon
    tray_icon = QSystemTrayIcon(QIcon(APP_ICON), parent=app)
    tray_icon.setToolTip(f"{APP_NAME} – Click to adjust brightness")

    # Context menu
    tray_menu = QMenu()
    show_action = QAction("Open MonitorGlow")
    show_action.triggered.connect(slider.fade_in)
    tray_menu.addAction(show_action)
    tray_menu.addSeparator()

    about_action = QAction("About")
    about_action.triggered.connect(slider.show_about)
    tray_menu.addAction(about_action)

    donate_action = QAction("Donate")
    donate_action.triggered.connect(slider.show_donate)
    tray_menu.addAction(donate_action)

    help_action = QAction("Help")
    help_action.triggered.connect(slider.show_help)
    tray_menu.addAction(help_action)

    tray_menu.addSeparator()
    exit_action = QAction("Exit")
    exit_action.triggered.connect(app.quit)
    tray_menu.addAction(exit_action)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.activated.connect(lambda reason: slider.fade_in() if reason == QSystemTrayIcon.Trigger else None)
    tray_icon.show()

    # Show notification message when opening the app
    notification_message()
    tray_icon.showMessage(
        f"{APP_NAME} – {AUTHOR} by {APP_DEVELOPER}",
        "Running in background.\nAccess it from the system tray.",
        QSystemTrayIcon.Information,
        5000  # Duration in milliseconds
    )
    # ---------------------------------------------

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
