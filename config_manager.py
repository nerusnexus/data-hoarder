import os
import json

CONFIG_FILE = "config.json"
DEFAULT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Root")

class ConfigManager:
    @staticmethod
    def load_config():
        if not os.path.exists(CONFIG_FILE):
            return {"root_path": DEFAULT_ROOT}
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                # Ensure key exists
                if "root_path" not in data:
                    data["root_path"] = DEFAULT_ROOT
                return data
        except Exception as e:
            print(f"Error loading config: {e}")
            return {"root_path": DEFAULT_ROOT}

    @staticmethod
    def save_config(data):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    @staticmethod
    def get_root_path():
        return ConfigManager.load_config().get("root_path", DEFAULT_ROOT)

    @staticmethod
    def set_root_path(path):
        data = ConfigManager.load_config()
        data["root_path"] = path
        ConfigManager.save_config(data)
