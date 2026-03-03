import pygame
import math
from engine import colors

class Player(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pygame.Surface((50, 50))
        self.image.fill(colors.red)
        self.rect = self.image.get_rect()

        self.speed = 300
        self.jumpForce = 600
        self.gravity = 9.8 * 60

        self.friction = 0.85

        self.position = pygame.math.Vector2(0, 0)

        self.acceleration = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)

        self.grounded = False

        self.debugActive = False

    def debug_print(self, *message):
        if self.debugActive:
            print(message)

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acceleration.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acceleration.x += self.speed
        if keys[pygame.K_SPACE]:
            self.velocity.y = -self.jumpForce
            self.debug_print("Jumping")

    def round_away_from_zero(self, n):
        if n > 0:
            return math.ceil(n)
        elif n < 0:
            return math.floor(n)
        else:
            return 0
    
    def move_with_collision(self, vel, blocks):
        nextPosRect = self.rect.move(vel.x, vel.y)
        self.debug_print(self.rect.right, self.rect.bottom)
        self.debug_print(nextPosRect.right, nextPosRect.bottom)

        collidedX = False
        collidedY = False

        grounded = False
        for block in blocks:
            if not nextPosRect.colliderect(block.rect):
                continue

            self.debug_print("Colliding with block")
            self.debug_print(block.rect.left, block.rect.top)
            self.debug_print(self.rect.right, self.rect.bottom)
            self.debug_print(vel.x, vel.y)

            # going right
            if vel.x > 0:
                self.debug_print("Colliding with block going right")
                nextPosRect.right = block.rect.left
                vel.x = 0
                collidedX = True
            # going left
            elif vel.x < 0:
                self.debug_print("Colliding with block going left")
                nextPosRect.left = block.rect.right
                vel.x = 0
                collidedX = True
            # going down
            if vel.y > 0:
                self.debug_print("Colliding with block going down")
                nextPosRect.bottom = block.rect.top
                vel.y = 0
                grounded = True
                collidedY = True
            # going up
            elif vel.y < 0:
                self.debug_print("Colliding with block going up")
                nextPosRect.top = block.rect.bottom
                vel.y = 0
                collidedY = True
        return grounded, vel, nextPosRect, collidedX, collidedY

    def update(self, dt, blocks=[]):
        dt /= 1000
        self.debug_print("Updating player")
        self.debug_print(f"dt: {dt}")

        self.debug_print(f"self.acceleration: {self.acceleration}, self.velocity: {self.velocity}")

        # check if still grounded
        if self.grounded:
            self.grounded = self.move_with_collision(pygame.math.Vector2(0, 1), blocks)[0]

        # check if gravity should be applied
        if not self.grounded:
            self.debug_print("Applying gravity")
            self.acceleration.y += self.gravity
        self.velocity += self.acceleration * dt
        self.debug_print(f"acceleration: {self.acceleration}, velocity: {self.velocity}")

        # vertical movement and collision
        grounded, endVel, endRect, _, collidedY = self.move_with_collision(pygame.math.Vector2(0, self.round_away_from_zero(self.velocity.y * dt)), blocks)
        # if collided, snap, else move normally
        if collidedY:
            self.rect.y = endRect.y
            self.position.y = self.rect.y
            self.velocity.y = endVel.y

            if grounded and not self.grounded:
                self.grounded = True
                self.debug_print("Landed")
        else:
            self.position.y += self.velocity.y * dt
            # pygame already rounds it, maybe it should be round_away_from_zero instead? would give more accurate visuals i think
            self.rect.y = int(self.position.y)
        
        self.debug_print("\nvertical check")
        self.debug_print(f"collidedY: {collidedY}")
        self.debug_print(f"self.grounded: {self.grounded}")
        self.debug_print(f"self.position: {self.position}")
        self.debug_print(f"self.velocity: {self.velocity}")

        # horizontal movement and collision
        _, endVel, endRect, collidedX, _ = self.move_with_collision(pygame.math.Vector2(self.round_away_from_zero(self.velocity.x * dt), 0), blocks)
        # if collided, snap, else move normally
        if collidedX:
            self.rect.x = endRect.x
            self.position.x = self.rect.x
            self.velocity.x = endVel.x
        else:
            self.position.x += self.velocity.x * dt
            # pygame already rounds it, maybe it should be round_away_from_zero instead? would give more accurate visuals i think
            self.rect.x = int(self.position.x)

        self.debug_print("\nhorizontal check")
        self.debug_print(f"collidedX: {collidedX}")
        self.debug_print(f"self.position: {self.position}")
        self.debug_print(f"self.velocity: {self.velocity}")
        self.debug_print("--------------")

        self.acceleration = pygame.math.Vector2(0, 0)
        self.velocity.x -= self.velocity.x * self.friction * dt

    def render(self, surface):
        surface.blit(self.image, self.rect)
