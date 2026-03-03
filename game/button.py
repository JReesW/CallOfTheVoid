import pygame
from engine import colors

class Button(pygame.sprite.Sprite):
    def __init__(self, size, position, gates = [], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pygame.Surface(size)
        self.image.fill(colors.indigo)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.gates = gates

        self.pressed = False

    def update(self, dt):
        pass

    def collide(self, objects):
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if self.pressed:
                    return True
                self.pressed = True

                bottom = self.rect.bottom
                self.rect.height /= 3
                self.rect.bottom = bottom

                self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
                self.image.fill(colors.purple)

                for gate in self.gates:
                    gate.buttonsPressed += 1

                return True
        return False
    
    def render(self, surface):
        surface.blit(self.image, self.rect)