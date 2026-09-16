import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox

from config.app_config import APP_DEVELOPER, APP_ICON, APP_NAME, APP_VERSION, AUTHOR


def resource_path(relative_path):
    """Get absolute path to a resource for development and PyInstaller builds."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def notification_message():
    msg_box = QMessageBox()
    msg_box.setWindowTitle(f"{APP_NAME} – {AUTHOR} by {APP_DEVELOPER} v{APP_VERSION}")
    msg_box.setText(
        f"{APP_NAME} is now running in the background.\n"
        "You can access it from the system tray."
    )

    msg_box.setWindowIcon(QIcon(APP_ICON))
    msg_box.setIconPixmap(
        QPixmap(APP_ICON).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    )
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setStyleSheet(
        """
        QWidget {
            font-size: 11pt;
            color: white;
            background-color: #2b2b2b;
        }
        QLabel {
            padding: 5px;
        }
        QPushButton {
            background-color: #444;
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #666;
        }
        """
    )
    msg_box.exec_()
