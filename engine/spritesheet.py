import pygame
import json


class SpriteSheet:
    """
    A sprite sheet, consisting of an image and a .json file located in "resources/spritesheets/"
    """
    
    def __init__(self, name: str):
        self.sprites = None
        self.sheet_info = None

        self.load(name)

    def get_sprite(self, sprite: str, flip: bool = False) -> pygame.Surface:
        """
        Get a sprite by its name
        """
        if flip: sprite += 'F'
        return self.sprites[sprite]

    def load(self, name: str):
        """
        Load all the sprite sheet info in
        """
        surface = pygame.image.load(f"resources/spritesheets/{name}.png").convert_alpha()
        with open(f"resources/spritesheets/{name}.json") as f:
            sheet_info = json.load(f)
        
        if sheet_info["usesColorKey"]:
            surface.set_colorkey(sheet_info["colorKey"])
        
        sprites = {}
        for name, (x, y, w, h) in sheet_info["sprites"].items():
            rect = pygame.Rect(x, y, w, h)
            sprite = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
            sprite.blit(surface, (0, 0), rect)
            sprites[name] = sprite
            if sheet_info["flipAll"]:
                sprites[name + 'F'] = pygame.transform.flip(sprite, True, False)

        self.sprites = sprites
        self.sheet_info = sheet_info
