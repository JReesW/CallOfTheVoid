import os
import sys
import platformdirs


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


def get_save_path(filename: str):
    """
    Return the given filename appended to the save data path
    """
    base_dir = platformdirs.user_data_dir("CallOfTheVoid", "JReesW")

    os.makedirs(base_dir, exist_ok=True)

    return os.path.join(base_dir, filename)
