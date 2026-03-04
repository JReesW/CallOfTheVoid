import pygame
import math
from engine import colors, debug


class Player(pygame.sprite.Sprite):
    def __init__(self, start: tuple[int, int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pygame.Surface((50, 50))
        self.image.fill(colors.red)
        self.rect = pygame.Rect(start[0] * 48, start[1] * 48, 50, 50)

        self.speed = 5
        self.jump_force = 12
        self.gravity = -15

        self.velocity = pygame.math.Vector2(0, 0)

        self.grounded = False

    def handle_events(self, events):        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.velocity.x -= self.speed
                if event.key == pygame.K_d:
                    self.velocity.x += self.speed
                if event.key == pygame.K_SPACE and self.grounded:
                    self.velocity.y = -self.jump_force
                    self.grounded = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.velocity.x += self.speed
                if event.key == pygame.K_d:
                    self.velocity.x -= self.speed

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

    def update(self, dt: float, blocks: list[pygame.Rect]):
        dt /= 1000
        if not self.grounded:
            self.velocity.y -= self.gravity * dt
        else:
            self.velocity.y = 1
        self.move_and_collide(self.velocity.x, self.velocity.y, blocks)

    def render(self, surface):
        surface.blit(self.image, self.rect)
