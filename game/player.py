import pygame
import math


from engine import colors, debug, spritesheet, animation
from game.level import Level


class Player(pygame.sprite.Sprite):
    def __init__(self, level: Level, shadow: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.shadow = shadow
        self.level = level
        self.spritesheet = spritesheet.SpriteSheet("shadow" if shadow else "player")
        self.animation_handler = animation.AnimationHandler(self.spritesheet)
        self.animation_handler.play("idle")
        self.image = self.animation_handler.get_frame()

        self.rect = pygame.FRect(level.start[0] * 48, level.start[1] * 48, 48, 96)

        self.speed = 5
        self.jump_force = 12
        self.gravity = -15

        self.velocity = pygame.math.Vector2(0, 0)

        self.grounded = False
        self.looking_left = False
        self.climbing = False

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.velocity.x = -self.speed / (2 if self.climbing else 1)
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.velocity.x = self.speed / (2 if self.climbing else 1)
        else:
            self.velocity.x = 0
        
        if keys[pygame.K_w] and self.on_ladder():
            self.climbing = True
            self.velocity.y = -3
        elif keys[pygame.K_s] and self.on_ladder():
            self.climbing = True
            self.velocity.y = 3
        elif self.on_ladder() and self.climbing:
            self.velocity.y = 0

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (self.grounded or self.climbing):
                    self.velocity.y = -self.jump_force
                    self.grounded = False
                    self.climbing = False

    def update(self, dt: float):
        blocks = self.level.blocks

        dt_s = dt / 1000  # delta time in seconds
        if not self.grounded and not self.climbing:
            self.velocity.y -= self.gravity * dt_s
        elif not self.climbing:
            self.velocity.y = 1
        self.move_and_collide(self.velocity.x, self.velocity.y, blocks)
        if not self.on_ladder(): self.climbing = False

        # Animation stuff
        if self.velocity.x < 0: self.looking_left = True
        if self.velocity.x > 0: self.looking_left = False
        if self.climbing and self.velocity.y != 0: self.animation_handler.play("climb")
        elif self.climbing: self.animation_handler.play("climb_idle")
        elif self.velocity.x != 0 and self.grounded: self.animation_handler.play("run", flip=self.looking_left)
        elif self.grounded: self.animation_handler.play("idle", flip=self.looking_left)
        elif self.velocity.y < 0: self.animation_handler.play("jump", flip=self.looking_left)
        elif self.velocity.y > 0: self.animation_handler.play("fall", flip=self.looking_left)
        
        self.animation_handler.update(dt)
        self.image = self.animation_handler.get_frame()

    def render(self, surface):
        surface.blit(self.image, self.rect)
    
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
    
    def on_ladder(self) -> bool:
        return self.rect.collidelist(self.level.ladder_blocks) != -1
