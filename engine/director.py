import pygame

from engine.scene import Scene

import scenes


__scenes: dict[str, Scene] = {}
scene: Scene = None
next_scene: Scene = None


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
    Load all scene classes defined in the scenes module
    """
    for scene in scenes.scenes:
        __scenes[scene.__name__] = scene


def quit() -> None:
    """
    Post a quit event to quit the game
    """
    pygame.event.post(pygame.Event(pygame.QUIT))
