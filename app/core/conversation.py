from PyQt5.QtCore import QObject, pyqtSignal
import random


class ConversationManager(QObject):
    response_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.context = {}

    def handle_response(self, command, result, success):
        if not success:
            return random.choice([
                f"I couldn't complete: {command}",
                f"Failed to execute: {command}",
                result  # Use the error message from handler
            ])

        responses = {
            'open': [
                f"I've opened {command.replace('open', '').strip()} for you",
                f"Launching {command.replace('open', '').strip()}",
                f"{command.replace('open', '').strip()} is now open"
            ],
            'default': [
                "Task completed",
                "Done",
                "Command executed"
            ]
        }

        key = 'open' if 'open' in command else 'default'
        return random.choice(responses[key])