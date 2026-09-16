import logging

from PyQt5.QtCore import QEasingCurve, QObject, QPropertyAnimation, QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from config.app_config import APP_DEVELOPER, APP_NAME, APP_VERSION, AUTHOR
from core.display_service import DisplayCommandService
from core.monitor import ScreenBrightnessBackend
from dialogs.About_Dialog import AboutDialog
from dialogs.Donate_Dialog import DonateDialog
from dialogs.Help_Dialog import HelpDialog

logger = logging.getLogger(__name__)


class _DisplaySignals(QObject):
    displays_ready = pyqtSignal(object)
    brightness_ready = pyqtSignal(str, object)
    brightness_written = pyqtSignal(str, int, object)


class MonitorGlow(QWidget):
    def __init__(self, backend=None, service=None):
        super().__init__()
        self.backend = backend or ScreenBrightnessBackend()
        self.display_service = service or DisplayCommandService(self.backend)
        self.displays = []
        self._updating_slider = False
        self._signals = _DisplaySignals(self)
        self._signals.displays_ready.connect(self._apply_display_result)
        self._signals.brightness_ready.connect(self._apply_brightness_result)
        self._signals.brightness_written.connect(self._apply_write_result)

        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(3000)
        self._refresh_timer.timeout.connect(self.refresh_displays)
        self._refresh_timer.start()

        app = QApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(self.shutdown)

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
        buttons = (
            ("About", self.show_about),
            ("Donate", self.show_donate),
            ("Help", self.show_help),
        )
        for name, callback in buttons:
            btn = QPushButton(name)
            btn.clicked.connect(callback)
            btn.setStyleSheet(
                "padding: 6px; background-color: #444; border-radius: 6px;"
            )
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.refresh_displays()

    def refresh_displays(self):
        try:
            future = self.display_service.list_displays()
        except RuntimeError:
            return
        future.add_done_callback(self._display_query_finished)

    def _display_query_finished(self, future):
        try:
            result = future.result()
        except Exception as exc:
            result = exc
        self._signals.displays_ready.emit(result)

    def _apply_display_result(self, result):
        if isinstance(result, Exception):
            logger.warning("Cannot enumerate displays: %s", result)
            displays = []
        else:
            displays = result

        selected_id = None
        selected = self._selected_display()
        if selected is not None:
            selected_id = selected.id

        current_ids = [display.id for display in self.displays]
        new_ids = [display.id for display in displays]
        self.displays = displays
        if current_ids == new_ids and self.monitor_selector.count() == len(displays):
            return

        self.monitor_selector.blockSignals(True)
        self.monitor_selector.clear()
        self.monitor_selector.addItems([display.name for display in displays])
        if selected_id in new_ids:
            self.monitor_selector.setCurrentIndex(new_ids.index(selected_id))
        self.monitor_selector.blockSignals(False)

        enabled = bool(displays)
        self.monitor_selector.setEnabled(enabled)
        self.slider.setEnabled(enabled)
        self.label.setText(
            "Set Brightness" if enabled else "No controllable display detected"
        )
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
            future = self.display_service.get_brightness(display.id)
        except RuntimeError:
            return
        future.add_done_callback(
            lambda completed, display_id=display.id: self._brightness_query_finished(
                display_id, completed
            )
        )

    def _brightness_query_finished(self, display_id, future):
        try:
            result = future.result()
        except Exception as exc:
            result = exc
        self._signals.brightness_ready.emit(display_id, result)

    def _apply_brightness_result(self, display_id, result):
        display = self._selected_display()
        if display is None or display.id != display_id:
            return
        if isinstance(result, Exception):
            logger.warning("Cannot read brightness: %s", result)
            self.label.setText("Brightness unavailable")
            return
        self._updating_slider = True
        self.slider.setValue(result)
        self._updating_slider = False
        self.label.setText(f"Brightness: {result}%")

    def set_brightness(self, value):
        if self._updating_slider:
            return
        display = self._selected_display()
        if not display:
            return
        self.label.setText(f"Brightness: {value}%")
        try:
            self.display_service.set_brightness(
                display.id,
                value,
                callback=lambda completed, display_id=display.id, requested=value: (
                    self._brightness_write_finished(
                        display_id,
                        requested,
                        completed,
                    )
                ),
            )
        except RuntimeError:
            logger.warning("Brightness request ignored after display service shutdown")

    def _brightness_write_finished(self, display_id, value, future):
        try:
            future.result()
            result = None
        except Exception as exc:
            result = exc
        self._signals.brightness_written.emit(display_id, value, result)

    def _apply_write_result(self, display_id, value, error):
        display = self._selected_display()
        if display is None or display.id != display_id:
            return
        if error is not None:
            logger.warning("Cannot set brightness: %s", error)
            self.label.setText("Brightness change failed")
        elif self.slider.value() == value:
            self.label.setText(f"Brightness: {value}%")

    def shutdown(self):
        self._refresh_timer.stop()
        self.display_service.shutdown(wait=False)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

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
