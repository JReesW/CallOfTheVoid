import pygame

from engine.scene import Scene

scene = None


def set_scene(_scene: Scene, *args, **kwargs) -> None:
    """
    Set the current scene to the given scene
    """
    global scene
    scene = _scene(*args, **kwargs)


def quit() -> None:
    pygame.event.post(pygame.Event(pygame.QUIT))
