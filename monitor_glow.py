import logging

from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QSlider, QVBoxLayout, QWidget

from config.app_config import APP_DEVELOPER, APP_NAME, APP_VERSION, AUTHOR
from core.display_backend import DisplayError
from core.display_service import DisplayCommandService
from core.monitor import ScreenBrightnessBackend
from dialogs.About_Dialog import AboutDialog
from dialogs.Donate_Dialog import DonateDialog
from dialogs.Help_Dialog import HelpDialog

logger = logging.getLogger(__name__)


class MonitorGlow(QWidget):
    brightness_applied = pyqtSignal(int)
    brightness_failed = pyqtSignal(str)

    def __init__(self, backend=None):
        super().__init__()
        self.backend = backend or ScreenBrightnessBackend()
        self.display_service = DisplayCommandService(self.backend)
        self.displays = []
        self._updating_slider = False
        self.brightness_applied.connect(self._on_brightness_applied)
        self.brightness_failed.connect(self._on_brightness_failed)
        self.setWindowTitle(f"{APP_NAME} - {AUTHOR} by {APP_DEVELOPER} v{APP_VERSION}")
        self.setFixedSize(320, 160)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self._apply_dark_palette()
        self._create_widgets()
        self.hide()

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
        self.monitor_selector.currentIndexChanged.connect(self.update_slider)

        self.label = QLabel("Set Brightness")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.set_brightness)

        layout.addWidget(self.monitor_selector)
        layout.addWidget(self.label)
        layout.addWidget(self.slider)

        btn_layout = QHBoxLayout()
        for name, callback in (("About", self.show_about), ("Donate", self.show_donate), ("Help", self.show_help)):
            btn = QPushButton(name)
            btn.clicked.connect(callback)
            btn.setStyleSheet("padding: 6px; background-color: #444; border-radius: 6px;")
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.refresh_displays()

    def refresh_displays(self):
        try:
            self.displays = self.backend.list_displays()
        except DisplayError as exc:
            logger.warning("Cannot enumerate displays: %s", exc)
            self.displays = []
        self.monitor_selector.clear()
        self.monitor_selector.addItems([display.name for display in self.displays])
        enabled = bool(self.displays)
        self.monitor_selector.setEnabled(enabled)
        self.slider.setEnabled(enabled)
        self.label.setText("Set Brightness" if enabled else "No controllable display detected")
        if enabled:
            self.update_slider()

    def _selected_display(self):
        index = self.monitor_selector.currentIndex()
        return self.displays[index] if 0 <= index < len(self.displays) else None

    def update_slider(self):
        display = self._selected_display()
        if not display:
            return
        try:
            brightness = self.backend.get_brightness(display.id)
        except DisplayError as exc:
            logger.warning("Cannot read brightness: %s", exc)
            self.label.setText("Brightness unavailable")
            return
        self._updating_slider = True
        self.slider.setValue(brightness)
        self._updating_slider = False
        self.label.setText(f"Brightness: {brightness}%")

    def set_brightness(self, value):
        if self._updating_slider:
            return
        display = self._selected_display()
        if not display:
            return
        self.label.setText(f"Brightness: {value}%")
        self.display_service.set_brightness(
            display.id,
            value,
            on_success=self.brightness_applied.emit,
            on_error=lambda exc: self.brightness_failed.emit(str(exc)),
        )

    def _on_brightness_applied(self, value):
        self.label.setText(f"Brightness: {value}%")

    def _on_brightness_failed(self, message):
        logger.warning("Cannot set brightness: %s", message)
        self.label.setText("Brightness change failed")

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def shutdown(self):
        """Release background display resources before application exit."""
        self.display_service.close()

    def fade_in(self):
        self.setWindowOpacity(0)
        self.show()
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(300)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        self._fade_anim = anim

    def show_help(self):
        self._exec_dialog(HelpDialog, "Help")

    def show_about(self):
        self._exec_dialog(AboutDialog, "About")

    def show_donate(self):
        self._exec_dialog(DonateDialog, "Donate")

    def _exec_dialog(self, dialog_type, name):
        try:
            dialog = dialog_type(parent=self)
            dialog.setModal(True)
            dialog.exec_()
        except Exception:
            logger.exception("Error opening %s dialog", name)
