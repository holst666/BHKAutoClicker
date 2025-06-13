import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller/Nuitka."""
    if hasattr(sys, '_MEIPASS'):
        # If running as EXE (PyInstaller or Nuitka)
        base_path = sys._MEIPASS
    else:
        # If running as script, use script's directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)