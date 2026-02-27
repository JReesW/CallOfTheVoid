import os
import sys


def get_path(relative_path: str):
    """
    Return the correct path for a given relative path.
    Mainly relevant for when working with PyInstaller.
    """
    
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)
