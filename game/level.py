import pygame
import json
from pathlib import Path

from engine.spritesheet import SpriteSheet
from engine.util import get_path


def generate_level_surface(spritesheet: SpriteSheet, tilemap: list[list[str]]) -> pygame.Surface:
    """
    Generate a prerender of a level's tilemap
    """
    surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)
    for r, row in enumerate(tilemap):
        for c, tile in enumerate(row):
            if tile:
                y = -12 + 48 * r
                x = 48 * c
                surface.blit(spritesheet.get_sprite(tile), (x, y))
    return surface


class Level:
    """
    Object representing everything about a level
    """

    def __init__(self, sheet: str, tilemap: list[list[str]]):
        self.spritesheet = SpriteSheet(sheet)
        self.tilemap = tilemap
        self.surface = generate_level_surface(self.spritesheet, tilemap)
    
    def redraw(self):
        self.surface = generate_level_surface(self.spritesheet, self.tilemap)


def load_level(name: str) -> Level:
    """
    Load a level by its filename in resources/levels
    """
    file_path = Path(get_path(f"resources/levels/{name}.json"))
    if file_path.exists():
        with open(file_path) as f:
            level_info = json.load(f)
    else:
        level_info = {
            "spritesheet": "cave",
            "tilemap": [
                ["CTL", *(["B"] * 38), "CTR"],
                *([["MR", *([""] * 38), "ML"]] * 21),
                ["CBL", *(["T"] * 38), "CBR"]
            ]
        }
        print(level_info)
    
    level = Level(level_info["spritesheet"], level_info["tilemap"])
    return level
