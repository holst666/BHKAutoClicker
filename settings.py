import configparser
import os
from util import resource_path

SETTINGS_FILE = resource_path("settings.cfg")

def save_settings(settings):
    config = configparser.ConfigParser()
    config["main"] = settings
    with open(SETTINGS_FILE, "w") as f:
        config.write(f)

def load_settings():
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