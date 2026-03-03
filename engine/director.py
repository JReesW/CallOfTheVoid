import pygame
from pathlib import Path
import os
import importlib
import inspect

from engine.scene import Scene
from engine.util import get_path


__scenes = {}
scene = None
next_scene = None


def change_scene(_scene: str, *args, **kwargs) -> None:
    """
    Change the current scene to the given scene on the next frame
    """
    global next_scene
    next_scene = __scenes[_scene](*args, **kwargs)


def _set_scene() -> None:
    global scene, next_scene
    scene = next_scene
    next_scene = None


def find_scenes(path: str = "scenes") -> None:
    """
    Automatically loads all scene classes found in the scenes folder
    """
    module_path = Path(get_path(path))

    # Check every file in the scenes module
    for file in os.listdir(module_path):
        # If it's a python file that isn't marked as protected
        if file.endswith('.py') and not file.startswith('__'):
            module_name = f".{file[:-3]}"
            relative_path = str(path).replace('/', '.')

            try:
                # Import the scene file
                module = importlib.import_module(module_name, package=relative_path)

                # Check for Scene derived classes, and store them
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, Scene) and obj is not Scene:
                        __scenes[name] = obj
            except Exception as e:
                print(f"Error loading Scene from {module_name}: {e}")


def quit() -> None:
    """
    Post a quit event to quit the game
    """
    pygame.event.post(pygame.Event(pygame.QUIT))
