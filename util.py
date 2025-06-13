import os, sys

def resource_path(relative_path):
    # Get absolute path to resource, works for dev and PyInstaller EXE
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)