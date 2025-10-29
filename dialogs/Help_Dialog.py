# dialogs/Help_Dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextBrowser, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from config.app_config import APP_NAME
import os
import resources_rc

class HelpDialog(QDialog):
    """Help dialog for MonitorGlow"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Help – {APP_NAME}")
        self.setFixedSize(460, 360)
        self.setModal(True)
        self.setStyleSheet(self._stylesheet())
        self.setWindowIcon(QIcon(":/assets/icons/help_icon.png"))

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        layout.addWidget(self._create_title_label())
        layout.addWidget(self._create_help_text())
        layout.addWidget(self._create_close_button(), alignment=Qt.AlignRight)

        self.setLayout(layout)

    def _create_title_label(self):
        label = QLabel(f"<b>{APP_NAME} – Help Guide</b>")
        label.setAlignment(Qt.AlignCenter)
        label.setTextFormat(Qt.RichText)
        label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        return label

    def _create_help_text(self):
        text = QTextBrowser()
        text.setFont(QFont("Segoe UI", 9))
        text.setOpenExternalLinks(True)
        text.setHtml(
            f"""
            <p><b>{APP_NAME}</b></p>
            <p><b>A Multi-Monitor Brightness Controller</b></p>
            <ul>
                <li>Use the slider to adjust your monitor’s brightness.</li>
                <li>Select the correct display if you have multiple monitors.</li>
                <li>The app minimizes to the system tray and runs in the background.</li>
                <li>Use <b>About</b> to learn more or <b>Donate</b> to support development.</li>
                <li>You can enable auto-start on Windows login via settings.</li>
            </ul>
            <p><b>All features run offline. No internet access is required.</b></p>
            """
        )
        text.setMinimumHeight(200)
        text.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #88c0d0;
                padding: 8px;
                border-radius: 6px;
            }
        """)
        return text

    def _create_close_button(self):
        btn = QPushButton("✖ Close")
        btn.setFixedWidth(100)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setShortcut("Esc")
        btn.clicked.connect(self.accept)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: #88c0d0;
                border: 1px solid #88c0d0;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                border: 1px solid #a3d1e6;
                color: #a3d1e6;
            }
            QPushButton:pressed {
                background-color: #1f1f1f;
            }
        """)
        return btn

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)

    def _stylesheet(self):
        return """
        QWidget {
            font-size: 11pt;
            color: white;
            background-color: #2b2b2b;
        }
        QLabel {
            padding: 5px;
            border-radius: 6px;
            color: #88c0d0;
            font-size: 12pt;
        }
        """
