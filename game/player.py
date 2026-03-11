import pygame
import math


from engine import colors, debug, spritesheet, animation, director
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

        self.rect = pygame.FRect(level.start[0] * 48, (level.start[1] - 1) * 48, 48, 96)

        self.speed = 5
        self.jump_force = 12.3
        self.gravity = -15

        self.velocity = pygame.math.Vector2(0, 0)

        self.grounded = False
        self.looking_left = False
        self.climbing = False
        self.grabbed = None
        self.looking_up = False
        self.looking_down = False
        self.leaving_mark = False
        self.dead = False

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.velocity.x = -self.speed / (2 if self.climbing else 1)
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.velocity.x = self.speed / (2 if self.climbing else 1)
        else:
            self.velocity.x = 0
        
        if keys[pygame.K_w] and self.on_ladder() and self.grabbed is None:
            self.climbing = True
            self.velocity.y = -3
        elif keys[pygame.K_s] and self.on_ladder() and self.grabbed is None:
            self.climbing = True
            self.velocity.y = 3
        elif self.on_ladder() and self.climbing:
            self.velocity.y = 0
        
        self.looking_up = keys[pygame.K_w] and not keys[pygame.K_s] and not self.climbing
        self.looking_down = keys[pygame.K_s] and not keys[pygame.K_w] and not self.climbing

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (self.grounded or self.climbing):
                    self.velocity.y = -self.jump_force
                    self.grounded = False
                    self.climbing = False
                    director.audio.play_sound("jump")
                if event.key == pygame.K_e and self.grounded and not self.climbing:
                    can_press = True
                    if self.grabbed is None and not self.shadow:
                        self.grab_box()
                        if self.grabbed is not None: can_press = False
                    elif self.grabbed is not None and not self.shadow:
                        self.drop_box()
                        can_press = False
                    if can_press:
                        self.press_button()

    def update(self, dt: float, blocks: list[pygame.Rect], death_blocks: list[pygame.Rect]):
        if self.rect.collidelist(death_blocks) != -1:
            self.dead = True

        if not self.dead:
            if not self.grounded and not self.climbing:
                self.velocity.y -= self.gravity * (1/60)
            elif not self.climbing:
                self.velocity.y = 1
            self.move_and_collide(self.velocity.x, self.velocity.y, blocks)
            if not self.on_ladder(): self.climbing = False

        # Box carrying
        if self.grabbed is not None:
            x = self.rect.left - 8 if self.looking_left else self.rect.right + 8
            self.grabbed.rect.center = (x, self.rect.top + 32)

        # Animation stuff
        if self.velocity.x < 0: self.looking_left = True
        if self.velocity.x > 0: self.looking_left = False
        if self.dead: self.animation_handler.play("dead")
        elif self.climbing and self.velocity.y != 0: self.animation_handler.play("climb")
        elif self.climbing: self.animation_handler.play("climb_idle")
        elif self.velocity.x != 0 and self.grounded: self.animation_handler.play("run", flip=self.looking_left)
        elif self.looking_up and self.grounded: self.animation_handler.play("look_up", flip=self.looking_left)
        elif self.looking_down and self.grounded: self.animation_handler.play("look_down", flip=self.looking_left)
        elif self.grounded: self.animation_handler.play("idle", flip=self.looking_left)
        elif self.velocity.y < 0: self.animation_handler.play("jump", flip=self.looking_left)
        elif self.velocity.y > 0: self.animation_handler.play("fall", flip=self.looking_left)
        
        self.animation_handler.update(dt)
        self.image = self.animation_handler.get_frame()

    def render(self, surface):
        surface.blit(self.image, self.rect)
    
    def move_and_collide(self, dx: float, dy: float, blocks: list[pygame.Rect]):
        """
        Move the player and check for collision
        """
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

        # Horizontal
        self.rect.left += dx
        for block in blocks:
            if self.rect.colliderect(block):
                if dx > 0:
                    self.rect.right = block.left
                elif dx < 0:
                    self.rect.left = block.right
    
    def on_ladder(self) -> bool:
        """
        Return whether the player is colliding with a ladder hitbox
        """
        return self.rect.collidelist(self.level.ladder_blocks) != -1

    def grab_box(self):
        """
        Grab a box in front of the player
        """
        grab_block = pygame.Rect(0, 0, 32, 32)
        grab_block.bottom = self.rect.bottom - 12
        if self.looking_left:
            grab_block.right = self.rect.left - 8
        else:
            grab_block.left = self.rect.right + 8
        boxes = director.scene.boxes
        for box in boxes:
            if grab_block.colliderect(box):
                self.grabbed = box
                box.held = True

    def drop_box(self):
        """
        Drop a box in front of the player, if there's space to do so
        """
        x = self.rect.left - 24 if self.looking_left else self.rect.right + 24
        self.grabbed.rect.center = (x, self.rect.top + 24)
        if self.grabbed.rect.collidelist(self.level.blocks) == -1:
            self.grabbed.held = False
            self.grabbed.grounded = False
            self.grabbed = None

    def press_button(self):
        """
        Press a button
        """
        buttons = director.scene.buttons.values()
        for button in buttons:
            if self.rect.colliderect(button.rect):
                button.toggle()
                break
