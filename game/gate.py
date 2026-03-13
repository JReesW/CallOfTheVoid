import pygame

from engine import colors, image
from game.level import Level


"""
Gate rotation:
 0 = Extends upwards
 1 = Extends to the left
 2 = Extends downwards
 3 = Extends to the right
"""


class Gate(pygame.sprite.Sprite):
    def __init__(self, level: Level, start: tuple[int, int], rotation: int, length: int, inverted: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.level = level
        self.image = pygame.transform.rotate(image.load_image("gate").subsurface((0, 0, 48, 48*length)), rotation * 90)
        self.rect = pygame.FRect(0, 0, 0, 0)

        self.start = start
        self.rotation = rotation
        self.length = length
        self.inverted = bool(inverted)
        self.open = False
        self.inputs = {}
        self.dl = length

        self.calc_rect()

    def update(self):
        if self.open and self.dl > 0.5:
            self.dl = max(self.dl - 0.1, 0.5)
            self.calc_rect()
        elif not self.open and self.dl < self.length:
            self.dl = min(self.dl + 0.1, self.length)
            self.calc_rect()
    
    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect, (0, 0, *self.rect.size))
    
    def check_change(self):
        if all(self.inputs.values()):
            self.open = not self.inverted
        else:
            self.open = self.inverted
    
    def calc_rect(self):
        dl = 48 * self.dl
        if self.rotation == 0: self.rect = pygame.FRect(self.start[0] * 48, self.start[1] * 48 - 12 - dl + 48, 48, dl)
        if self.rotation == 1: self.rect = pygame.FRect(self.start[0] * 48 - dl + 48, self.start[1] * 48 - 12, dl, 48)
        if self.rotation == 2: self.rect = pygame.FRect(self.start[0] * 48, self.start[1] * 48 - 12, 48, dl)
        if self.rotation == 3: self.rect = pygame.FRect(self.start[0] * 48, self.start[1] * 48 - 12, dl, 48)