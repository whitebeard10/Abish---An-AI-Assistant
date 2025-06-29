import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from app.interfaces.gui.main_window import MainWindow
from app.core.command_handler import CommandHandler
from app.interfaces.voice_interface import VoiceInterface


class JARVIS:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.voice = VoiceInterface()
        self.handler = CommandHandler()
        self.gui = MainWindow(self)

        # Set up voice listening timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.listen_for_commands)
        self.timer.start(100)  # Check for commands every 100ms

    def listen_for_commands(self):
        command = self.voice.listen()
        if command:
            self.gui.update_signal.emit(f"Received command: {command}")
            self.handler.handle_command(command)

    def run(self):
        self.gui.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    jarvis = JARVIS()
    jarvis.run()