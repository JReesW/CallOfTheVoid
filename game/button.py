import pygame

from engine import colors, image
from game.level import Level


class Button(pygame.sprite.Sprite):
    def __init__(self, level: Level, start: tuple[int, int], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level = level
        self.image = image.load_image("button_off")
        self.rect = pygame.FRect(start[0] * 48, start[1] * 48 - 12, 48, 72)

        self.start = start
        self.pressed = False
        self.outputs = []
    
    def render(self, surface):
        surface.blit(self.image, self.rect)
    
    def toggle(self):
        self.pressed = not self.pressed
        self.image = image.load_image("button_on") if self.pressed else image.load_image("button_off")
        for output in self.outputs:
            output.inputs[self.start] = self.pressed
            output.check_change()