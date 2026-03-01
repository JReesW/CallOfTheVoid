import pygame
from engine import colors

class Block(pygame.sprite.Sprite):
    def __init__(self, size, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pygame.Surface(size)
        self.image.fill(colors.blue)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    
    def render(self, surface):
        surface.blit(self.image, self.rect)