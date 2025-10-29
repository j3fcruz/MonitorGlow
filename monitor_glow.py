# monitor_glow.py

import sys
from PyQt5.QtWidgets import (
    QWidget, QSlider, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

import screen_brightness_control as sbc

from dialogs.Donate_Dialog import DonateDialog
from dialogs.About_Dialog import AboutDialog
from dialogs.Help_Dialog import HelpDialog
from config.app_config import APP_NAME, APP_VERSION, APP_ICON, APP_DEVELOPER, AUTHOR


class MonitorGlow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {AUTHOR} by {APP_DEVELOPER} v{APP_VERSION}")
        self.setFixedSize(320, 160)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self._apply_dark_palette()
        self._create_widgets()
        self.hide()  # start hidden at boot

    def _apply_dark_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(60, 60, 60))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)
        self.setStyleSheet("""
            QWidget { font-size: 11pt; color: white; background-color: #2b2b2b; }
            QComboBox, QSlider, QLabel { padding: 5px; border-radius: 6px; }
            QSlider::groove:horizontal { height: 8px; background: #555; border-radius: 4px; }
            QSlider::handle:horizontal { width: 18px; background: #88c0d0; margin: -6px 0; border-radius: 9px; }
        """)

    def _create_widgets(self):
        layout = QVBoxLayout()

        self.monitor_selector = QComboBox()
        self.monitors = sbc.list_monitors()
        self.monitor_selector.addItems(self.monitors)
        self.monitor_selector.currentIndexChanged.connect(self.update_slider)

        self.label = QLabel("Set Brightness")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.set_brightness)

        layout.addWidget(self.monitor_selector)
        layout.addWidget(self.label)
        layout.addWidget(self.slider)

        # Buttons: About / Donate / Help
        btn_layout = QHBoxLayout()
        for name, callback in [("About", self.show_about),
                               ("Donate", self.show_donate),
                               ("Help", self.show_help)]:
            btn = QPushButton(name)
            btn.clicked.connect(callback)
            btn.setStyleSheet("padding: 6px; background-color: #444; border-radius: 6px;")
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.update_slider()

    def update_slider(self):
        try:
            current_monitor = self.monitor_selector.currentText()
            brightness = sbc.get_brightness(display=current_monitor)[0]
            self.slider.setValue(brightness)
        except Exception as e:
            print(f"Error fetching brightness: {e}")
            self.slider.setValue(50)

    def set_brightness(self, value):
        try:
            current_monitor = self.monitor_selector.currentText()
            sbc.set_brightness(value, display=current_monitor)
        except Exception as e:
            print(f"Error setting brightness: {e}")

    def closeEvent(self, event):
        event.ignore()  # Prevent exit on close
        self.hide()     # Just hide it to tray

    def fade_in(self):
        self.setWindowOpacity(0)
        self.show()
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(300)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        self._fade_anim = anim  # prevent garbage collection

    def show_help(self):
        try:
            dlg = HelpDialog(parent=self)
            dlg.setModal(True)
            dlg.exec_()
        except Exception as e:
            print(f"Error opening Help dialog: {e}")

    def show_about(self):
        try:
            dlg = AboutDialog(parent=self)
            dlg.setModal(True)
            dlg.exec_()
        except Exception as e:
            print(f"Error opening About dialog: {e}")

    def show_donate(self):
        try:
            dlg = DonateDialog(parent=self)
            dlg.setModal(True)
            dlg.exec_()
        except Exception as e:
            print(f"Error opening Donate dialog: {e}")
