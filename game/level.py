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


def generate_blocks(tilemap: list[list[str]], solid: list[str]) -> list[pygame.Rect]:
    """
    Generate collision blocks for clusters of solid tiles
    """
    width, height = len(tilemap[0]), len(tilemap)
    rects = []
    visited = set()

    for y in range(height):
        for x in range(width):
            if tilemap[y][x] in solid and (x, y) not in visited:
                # Find max width
                max_width = 0
                while x + max_width < width and tilemap[y][x + max_width] in solid and (x + max_width, y) not in visited:
                    max_width += 1

                # Find max height
                max_height = 1
                done = False

                while not done and y + max_height < height:
                    for dx in range(max_width):
                        if (tilemap[y + max_height][x + dx] not in solid or (x + dx, y + max_height) in visited):
                            done = True
                            break
                    if not done:
                        max_height += 1

                # Mark visited
                for dy in range(max_height):
                    for dx in range(max_width):
                        visited.add((x + dx, y + dy))

                # Save rectangle (convert to world coords)
                rects.append(pygame.Rect(x * 48, y * 48, max_width * 48, max_height * 48 - 12))

    return rects   


class Level:
    """
    Object representing everything about a level
    """

    def __init__(self, sheet: str, tilemap: list[list[str]], solid: list[str], start: tuple[int, int], end: tuple[int, int]):
        self.spritesheet = SpriteSheet(sheet)
        self.tilemap = tilemap
        self.surface = generate_level_surface(self.spritesheet, self.tilemap)
        self.solid = solid
        self.blocks = generate_blocks(self.tilemap, self.solid)
        self.start = start
        self.end = end
        self.place_doors()
    
    def redraw(self):
        self.surface = generate_level_surface(self.spritesheet, self.tilemap)
        self.place_doors()
    
    def place_doors(self):
        for x, y in [self.start, self.end]:
            left = (x-1) * 48
            top = (y-1) * 48 - 12
            w, h = 144, 144
            self.surface.fill((0, 0, 0, 0), pygame.Rect(left, top, w, h))
            self.surface.blit(self.spritesheet.get_sprite("DOOR"), (left, top))


def load_level(name: str) -> Level:
    """
    Load a level by its filename in resources/levels
    """
    file_path = Path(get_path(f"resources/levels/{name}.json"))
    if file_path.exists():
        with open(file_path) as f:
            level_info = json.load(f)
    else:
        # Default level template
        level_info = {
            "spritesheet": "cave",
            "tilemap": [
                ["CTL", *(["B"] * 38), "CTR"],
                *([["MR", *([""] * 38), "ML"]] * 21),
                ["CBL", *(["T"] * 38), "CBR"]
            ],
            "solid": ["TL", "T", "TR", "ML", "M", "MR", "BL", "B", "BR", "CTL", "CTR", "CBL", "CBR"],
            "start": [5, 22],
            "end": [34, 22]
        }
    
    level = Level(level_info["spritesheet"], level_info["tilemap"], level_info["solid"], level_info["start"], level_info["end"])
    return level
