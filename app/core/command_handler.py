import json
import subprocess
from pathlib import Path


class CommandHandler:
    def __init__(self):
        self.app_paths = self._load_app_paths()

    def _load_app_paths(self):
        path = Path(__file__).parent.parent / "utils" / "app_paths.json"
        with open(path) as f:
            return json.load(f)

    def handle_command(self, command):
        if not command or "open" not in command:
            return False

        app_name = command.replace("open", "").strip()
        return self.launch_app(app_name)

    def launch_app(self, app_name):
        if app_name in self.app_paths:
            subprocess.Popen(self.app_paths[app_name])
            return True
        return False