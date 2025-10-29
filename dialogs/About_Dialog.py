"""
About dialog for MonitorGlow
"""

import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from config.app_config import (
    APP_NAME, APP_VERSION, ABOUT_APP, COPYRIGHT, KOFI_LINK, DESCRIPTION, APP_ICON
)
import resources_rc


class AboutDialog(QDialog):
    """About dialog for MonitorGlow application."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_NAME}")
        self.setFixedSize(460, 480)
        self.setModal(True)
        self.setStyleSheet(self._dark_stylesheet())
        self.setWindowIcon(QIcon(":/assets/icons/about_icon.png"))
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(self._create_title_label())
        layout.addWidget(self._create_subtitle_label())
        layout.addWidget(self._create_version_label())
        layout.addWidget(self._create_description_box())
        layout.addWidget(self._create_dev_info_label())
        layout.addWidget(self._create_close_button(), alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def _create_title_label(self):
        label = QLabel(APP_NAME)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        return label

    def _create_subtitle_label(self):
        label = QLabel(ABOUT_APP)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 11))
        return label

    def _create_version_label(self):
        label = QLabel(f"Version: {APP_VERSION}")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 10))
        return label

    def _create_description_box(self):
        text_box = QTextBrowser()
        text_box.setOpenExternalLinks(True)
        text_box.setFont(QFont("Arial", 10))
        text_box.setHtml(self._format_description_html())
        text_box.setMinimumHeight(200)
        text_box.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #88c0d0;
                padding: 8px;
                border-radius: 6px;
            }
        """)
        return text_box

    def _format_description_html(self):
        html_desc = DESCRIPTION.replace("\n", "<br>")
        return f"""
            <p>{html_desc}</p>
            <p align="center" style="margin-top: 12px;">
                ❤️ Support us on 
                <a href="{KOFI_LINK}" 
                   style="color: orange; font-weight: bold; text-decoration: none;" 
                   target="_blank">
                   Ko-fi
                </a>
            </p>
        """

    def _create_dev_info_label(self):
        label = QLabel(COPYRIGHT)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 9))
        return label

    def _create_close_button(self):
        button = QPushButton("Close")
        button.setFixedWidth(100)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setStyleSheet("""
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
                color: #a3d1e6;
                border: 1px solid #a3d1e6;
            }
            QPushButton:pressed {
                background-color: #1f1f1f;
            }
        """)
        return button

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)

    def _dark_stylesheet(self):
        return """
        QWidget {
            background-color: #2b2b2b;
            color: white;
            font-family: Arial;
        }
        QLabel {
            font-size: 11pt;
        }
        """
