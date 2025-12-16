import json
import os
import sys

# AppData Integration
APP_NAME = "SmartFileOrganizer"
APP_DATA_DIR = os.path.join(os.getenv('LOCALAPPDATA'), APP_NAME)

# AppData Integration
APP_NAME = "SmartFileOrganizer"
APP_DATA_DIR = os.path.join(os.getenv('LOCALAPPDATA'), APP_NAME)

# Ensure directory exists
try:
    os.makedirs(APP_DATA_DIR, exist_ok=True)
    print(f"DEBUG: AppData Directory -> {APP_DATA_DIR}")
except OSError:
    # Fallback to current directory if AppData is not accessible
    APP_DATA_DIR = os.getcwd()
    print(f"DEBUG: AppData Failed. Fallback -> {APP_DATA_DIR}")

CONFIG_FILE = os.path.join(APP_DATA_DIR, "config.json")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

DEFAULT_CONFIG = {
    "language": "en",
    "agreed_to_terms": False
}

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return DEFAULT_CONFIG.copy()
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_CONFIG.copy()

    def get(self, key):
        return self.config.get(key, DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

config = ConfigManager()
