import pygame
from engine import colors

class Gate(pygame.sprite.Sprite):
    def __init__(self, size, position, buttonCount, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pygame.Surface(size)
        self.image.fill(colors.grey)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.buttonCount = buttonCount
        self.buttonsPressed = 0

        self.open = False

    def update(self, dt):
        if self.buttonsPressed == self.buttonCount:
            self.open = True
            self.image.fill(colors.green)
        else:
            self.open = False
            self.image.fill(colors.grey)
    
    def render(self, surface):
        surface.blit(self.image, self.rect)