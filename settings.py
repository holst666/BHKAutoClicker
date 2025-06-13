import configparser
import os
from util import resource_path
import shutil

SETTINGS_FILE = resource_path("settings.cfg")
DEFAULT_SETTINGS_FILE = resource_path("default_settings.cfg")

def ensure_settings_file():
    """Copy the default if the settings file is missing."""
    if not os.path.exists(SETTINGS_FILE):
        # Try to copy default to settings.cfg
        if os.path.exists(DEFAULT_SETTINGS_FILE):
            shutil.copy(DEFAULT_SETTINGS_FILE, SETTINGS_FILE)
        else:
            # Optionally, create a blank config if default is missing
            with open(SETTINGS_FILE, "w") as f:
                f.write("[main]\n")

def save_settings(settings):
    config = configparser.ConfigParser()
    config["main"] = settings
    with open(SETTINGS_FILE, "w") as f:
        config.write(f)

def load_settings():
    ensure_settings_file()
    config = configparser.ConfigParser()
    if not os.path.exists(SETTINGS_FILE):
        return {}
    config.read(SETTINGS_FILE)
    if "main" in config:
        return dict(config["main"])
    else:
        return {}

# === THESE HELPERS ARE NEEDED! ===

def str2bool(val):
    return str(val).lower() in ("1", "true", "yes", "on")

def getint(settings, key, default=0):
    try: return int(settings.get(key, default))
    except: return default

def getfloat(settings, key, default=0.0):
    try: return float(settings.get(key, default))
    except: return default

def getstr(settings, key, default=""):
    return settings.get(key, default)

def getpoint(settings, xkey, ykey):
    try:
        x = int(settings.get(xkey))
        y = int(settings.get(ykey))
        return (x, y)
    except:
        return None