import pygame

from engine import image
from game.level import Level


class Box(pygame.sprite.Sprite):
    def __init__(self, level: Level, start: tuple[int, int], *groups):
        super().__init__(*groups)

        self.level = level
        self.image = image.load_image("box")

        self.rect = pygame.FRect(start[0] * 48, start[1] * 48, 48, 48)

        self.gravity = -15

        self.velocity = pygame.math.Vector2(0, 0)

        self.grounded = False
        self.held = False
    
    def update(self, dt: float, blocks: list[pygame.Rect]):
        if not self.grounded and not self.held:
            self.velocity.y -= self.gravity * (1/60)
        elif not self.held:
            self.velocity.y = 1
        self.move_and_collide(self.velocity.x, self.velocity.y, blocks)

    def move_and_collide(self, dx: float, dy: float, blocks: list[pygame.Rect]):
        # Horizontal
        self.rect.left += dx
        for block in blocks:
            if self.rect.colliderect(block):
                if dx > 0:
                    self.rect.right = block.left
                elif dx < 0:
                    self.rect.left = block.right

        # Vertical
        self.rect.top += dy
        collided_with_floor = False
        for block in blocks:
            if self.rect.colliderect(block):
                if dy > 0:
                    collided_with_floor = True
                    self.rect.bottom = block.top
                    self.grounded = True
                elif dy < 0:
                    self.rect.top = block.bottom
                    self.velocity.y = 0
        if not collided_with_floor and dy > 0:
            self.grounded = False
