import sys
import os
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

from config.app_config import AUTHOR, APP_ICON, APP_NAME, APP_DEVELOPER, APP_VERSION

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def notification_message():
    msg_box = QMessageBox()
    msg_box.setWindowTitle(f"{APP_NAME} – {AUTHOR} by {APP_DEVELOPER} v{APP_VERSION}")
    msg_box.setText(f"{APP_NAME} is now running in the background.\nYou can access it from the system tray.")

    # Set window icon (top-left corner)
    msg_box.setWindowIcon(QIcon(APP_ICON))

    # Set custom icon inside the dialog (replaces QMessageBox.Information)
    msg_box.setIconPixmap(QPixmap(APP_ICON).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    msg_box.setStandardButtons(QMessageBox.Ok)

    # Custom dark style
    msg_box.setStyleSheet("""
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
    """)

    msg_box.exec_()
