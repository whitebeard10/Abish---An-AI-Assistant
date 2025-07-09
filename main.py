import sys
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from app.interfaces.gui.main_window import MainWindow
from app.core.command_handler import CommandHandler
from app.interfaces.voice_interface import VoiceInterface
from app.core.conversation import ConversationManager


class JARVIS:
    def __init__(self):
        # Initialize core components
        self.app = QApplication(sys.argv)
        self.voice = VoiceInterface()
        self.handler = CommandHandler()
        self.conversation = ConversationManager()

        # Setup GUI
        self.gui = MainWindow(self)

        # Connect signals
        self.conversation.response_ready.connect(self.handle_voice_response)
        self.gui.listening_state_changed.connect(self.on_listening_state_changed)

        # Initial voice greeting (after 1 second delay)
        QTimer.singleShot(1000, self.voice.speak_welcome)

        # Command processing timer
        self.command_timer = QTimer()
        self.command_timer.timeout.connect(self.process_commands)
        self.command_timer.start(100)  # Check every 100ms

        # Conversation state
        self.current_command = None
        self.waiting_for_followup = False

    def handle_listening_state(self, is_listening):
        """Handle GUI listening state changes"""
        if is_listening:
            self.voice.speak("I'm now listening for commands")

    def on_listening_state_changed(self, is_listening):
        """Handle listening state changes from GUI"""
        if is_listening:
            self.voice.speak("I'm now listening for commands")
            self.command_timer.start(100)
        else:
            self.command_timer.stop()

    def handle_voice_response(self, response):
        """Process voice responses from conversation manager"""
        self.voice.speak(response)
        self.waiting_for_followup = True
        QTimer.singleShot(2500, self.ask_followup_question)

    def ask_followup_question(self):
        """Ask if user needs anything else"""
        if self.waiting_for_followup and self.gui.is_listening:
            followups = [
                "Would you like anything else?",
                "What else can I do for you?",
                "Your next command, sir?",
                "How else may I assist?"
            ]
            self.voice.speak(random.choice(followups))
            self.waiting_for_followup = False

    def process_commands(self):
        """Main command processing loop"""
        if not self.gui.is_listening:
            return

        try:
            command = self.voice.listen(timeout=3)
            if command:
                self.current_command = command
                self.gui.update_signal.emit(f"Processing: {command}", "info")

                # Speak immediate acknowledgment
                self.voice.speak_confirmation(command)

                # Process command
                result, success = self.handler.handle_command(command)

                # Generate and emit response
                response = self.conversation.handle_response(
                    command,
                    result,
                    success
                )
                self.conversation.response_ready.emit(response)

        except Exception as e:
            self.gui.update_signal.emit(f"Error: {str(e)}", "error")

    def run(self):
        """Start the application"""
        self.gui.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    jarvis = JARVIS()
    jarvis.run()
    sys.exit(app.exec_())