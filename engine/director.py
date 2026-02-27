import pygame

from engine.scene import Scene

scene = None
next_scene = None


def change_scene(_scene: Scene, *args, **kwargs) -> None:
    """
    Change the current scene to the given scene on the next frame
    """
    global next_scene
    next_scene = _scene(*args, **kwargs)


def _set_scene() -> None:
    global scene, next_scene
    scene = next_scene
    next_scene = None


def quit() -> None:
    """
    Post a quit event to quit the game
    """
    pygame.event.post(pygame.Event(pygame.QUIT))
