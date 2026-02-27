from typing import Optional

import pygame
from engine import colors
from engine.util import get_path


__images = {}


def load_image(name: str, rotation: int = 0, size: Optional[tuple[int, int]] = None) -> pygame.Surface:
    """
    Load an image by its filename from the resources/images folder.
    Options include:
     - rotation in degrees
     - scaling to a given size
    """
    if name not in __images:
        __images[name] = pygame.image.load(get_path(f"resources/images/{name}.png")).convert_alpha()
    result = __images[name]
    if rotation != 0:
        result = pygame.transform.rotate(result, rotation)
    if size is not None:
        result = pygame.transform.scale(result, size)
    return result


def unload_image(name: str) -> None:
    """
    Unload an image by its name
    """
    if name in __images:
        del __images[name]


def unload_all_images() -> None:
    """
    Unload all currently loaded images
    """
    for name in list(__images.keys()):
        del __images[name]


def recolor(surf: pygame.Surface, color: colors.Color, special_flags: int = pygame.BLEND_RGBA_MAX) -> pygame.Surface:
    """
    Recolor the given surface to the given color using 
    """
    _surf = surf.copy()
    r, g, b, _ = color
    _surf.fill((r, g, b, 0), special_flags=special_flags)
    return _surf