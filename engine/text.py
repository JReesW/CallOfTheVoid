import pygame
import pygame.freetype

from engine import colors


if not pygame.freetype.get_init():
    pygame.freetype.init()


__font_names = {}
__fonts = {}


def render(text: str, color: colors.Color, font: str, size: int, bold: bool = False, italic: bool = False) -> tuple[pygame.Surface, pygame.Rect]:
    font = font.lower().replace(' ', '_')
    if (font, size) not in __fonts:
        if font in __font_names:
            __fonts[(font, size)] = pygame.freetype.Font(__font_names[font], size)
        else:
            __fonts[(font, size)] = pygame.freetype.SysFont(font, size, bold=bold, italic=italic)

    return __fonts[(font, size)].render(text, color)