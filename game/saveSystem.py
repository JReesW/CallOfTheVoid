import json
from pathlib import Path
from engine.util import get_path

saveData = None
defaultData = {"levelCleared": 0, "soundVolume": 1, "musicVolume": 1}

def load_save_data() -> dict:
    global saveData
    if saveData is not None:
        return saveData

    file_path = Path(get_path(f"resources/saves/save.json"))
    if file_path.exists():
        with open(file_path) as f:
            saveData = json.load(f)
            return saveData
    else:
        saveData = defaultData
        return saveData

def save_save_data(save_info: dict):
    global saveData
    saveData = save_info
    file_path = Path(get_path(f"resources/saves/save.json"))
    with open(file_path, "w") as f:
        json.dump(save_info, f, indent=4)