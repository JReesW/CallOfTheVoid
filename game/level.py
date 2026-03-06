import pygame
import json
from pathlib import Path

from engine.spritesheet import SpriteSheet
from engine.util import get_path
from engine import image


class Level:
    """
    Object representing everything about a level
    """

    def __init__(self, level_info):
        self.spritesheet = SpriteSheet(level_info["spritesheet"])
        self.tilemap = level_info["tilemap"]
        self.solid = level_info["solid"]
        self.start = level_info["start"]
        self.end = level_info["end"]
        self.ladders = level_info["ladders"]

        self.surface = self.generate_level_surface()
        self.blocks = self.generate_blocks()
        self.ladder_blocks = self.generate_ladder_blocks()
        self.place_doors()

    def generate_level_surface(self) -> pygame.Surface:
        """
        Generate a prerender of a level's tilemap
        """
        surface = pygame.Surface((1920, 1080), pygame.SRCALPHA)

        for x, y in self.ladders:
            surface.blit(image.load_image("ladder"), (x * 48, y * 48 - 12))

        for r, row in enumerate(self.tilemap):
            for c, tile in enumerate(row):
                if tile:
                    y = -12 + 48 * r
                    x = 48 * c
                    surface.blit(self.spritesheet.get_sprite(tile), (x, y))
        return surface

    def generate_blocks(self) -> list[pygame.Rect]:
        """
        Generate collision blocks for clusters of solid tiles
        """
        width, height = len(self.tilemap[0]), len(self.tilemap)
        rects = []
        visited = set()

        for y in range(height):
            for x in range(width):
                if self.tilemap[y][x] in self.solid and (x, y) not in visited:
                    # Find max width
                    max_width = 0
                    while x + max_width < width and self.tilemap[y][x + max_width] in self.solid and (x + max_width, y) not in visited:
                        max_width += 1

                    # Find max height
                    max_height = 1
                    done = False

                    while not done and y + max_height < height:
                        for dx in range(max_width):
                            if (self.tilemap[y + max_height][x + dx] not in self.solid or (x + dx, y + max_height) in visited):
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
    
    def generate_ladder_blocks(self) -> list[pygame.Rect]:
        """
        Generate blocks for ladder interaction
        """
        ladders = sorted(self.ladders)
        res = []
        current = None
        last = None

        for i, ladder in enumerate(ladders):
            if current is None:
                current = ladder
            else:
                if not (last[0] == ladder[0] and last[1] == ladder[1] - 1):
                    h = last[1] - current[1] + 1
                    res.append(pygame.Rect(current[0] * 48 + 8, current[1] * 48 - 12, 32, h * 48))
                    current = ladder
                if i == len(ladders) - 1:
                    h = ladder[1] - current[1] + 1
                    res.append(pygame.Rect(current[0] * 48 + 8, current[1] * 48 - 12, 32, h * 48))
                    current = ladder
            last = ladder
        
        return res

    def redraw(self):
        self.surface = self.generate_level_surface()
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
            "end": [34, 22],
            "ladders": []
        }
    
    level = Level(level_info)
    return level
