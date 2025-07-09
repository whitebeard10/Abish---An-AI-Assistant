from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QPushButton, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import os
import random


class MainWindow(QMainWindow):
    update_signal = pyqtSignal(str)
    listening_state_changed = pyqtSignal(bool)

    def __init__(self, jarvis_instance):
        super().__init__()
        self.jarvis = jarvis_instance
        self.setup_ui()
        self.setup_styles()
        self.connect_signals()

    def setup_ui(self):
        """Initialize all UI components"""
        self.setWindowTitle("JARVIS Assistant")
        self.setFixedSize(500, 400)

        # Main container
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Header
        self.header = QLabel("JARVIS Assistant")
        self.header.setAlignment(Qt.AlignCenter)

        # Status display
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        self.status_display.setPlaceholderText("System messages will appear here...")

        # Control buttons
        self.btn_listen = QPushButton("Start Listening")
        self.btn_exit = QPushButton("Exit")

        # Add widgets to layout
        layout.addWidget(self.header)
        layout.addWidget(self.status_display)
        layout.addWidget(self.btn_listen)
        layout.addWidget(self.btn_exit)

    def setup_styles(self):
        """Configure visual styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel, QTextEdit, QPushButton {
                color: #ffffff;
            }
            QTextEdit {
                background-color: #3c3f41;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                padding: 10px;
                border-radius: 5px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            #btn_exit {
                background-color: #f44336;
            }
            #btn_exit:hover {
                background-color: #d32f2f;
            }
        """)

        # Font settings
        font = QFont("Segoe UI", 12)
        self.header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.status_display.setFont(font)

        # Set button object names for specific styling
        self.btn_exit.setObjectName("btn_exit")

        # Set window icon (replace with your icon path)
        if os.path.exists("asset/icon.png"):
            self.setWindowIcon(QIcon("asset/icon.png"))

    def connect_signals(self):
        """Connect UI signals to slots"""
        self.btn_listen.clicked.connect(self.toggle_listening)
        self.btn_exit.clicked.connect(self.close)
        self.update_signal.connect(self.update_status)

    def toggle_listening(self):
        """Toggle listening state"""
        if self.btn_listen.text() == "Start Listening":
            self.btn_listen.setText("Stop Listening")
            self.update_status("Listening for commands...")
            # Start listening thread here
        else:
            self.btn_listen.setText("Start Listening")
            self.update_status("Standby mode")
            # Stop listening thread here

    def speak_welcome(self):
        welcome_msg = (
            "Initializing JARVIS systems. "
            "All protocols operational. "
            "How may I assist you today?"
        )
        return self.speak(welcome_msg)

    def speak_confirmation(self, command):
        confirmations = [
            f"Executing: {command}",
            f"Working on: {command}",
            f"Processing: {command}"
        ]
        return self.speak(random.choice(confirmations))

    def speak_followup(self):
        followups = [
            "Would you like anything else?",
            "What else can I do for you?",
            "Your next command, sir?",
            "How else may I assist?"
        ]
        return self.speak(random.choice(followups))

    def update_status(self, message):
        """Update status display with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_display.append(f"[{timestamp}] {message}")
        self.status_display.verticalScrollBar().setValue(
            self.status_display.verticalScrollBar().maximum()
        )

    def closeEvent(self, event):
        """Handle window close event"""
        self.update_status("Shutting down JARVIS...")
        # Cleanup operations here
        event.accept()