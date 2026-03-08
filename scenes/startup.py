import pygame
from engine.scene import Scene
from engine import colors, director
from engine.util import get_path

class StartupScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # current idea for animation
        # 0: fade in logo
        # 1: fade in text
        # 2: fade logo into color
        self.state = 0
        self.timer = 0
        self.paused = False

        self.logo = pygame.image.load(get_path(f"resources/images/teamlogo_splash_part0.png")).convert_alpha()
        self.text = pygame.image.load(get_path(f"resources/images/teamlogo_splash_part1.png")).convert_alpha()
        self.extra = pygame.image.load(get_path(f"resources/images/teamlogo_splash_part2.png")).convert_alpha()

        self.logoPos = (0, 0)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_RETURN:
                    self.state = 0
                    self.timer = 0

    def update(self, dt):
        if self.paused:
            return
        self.timer += dt / 1000
        if self.state == 0 and self.timer > 2:
            self.state = 1
            self.timer -= 2
        elif self.state == 1 and self.timer > 2:
            self.state = 2
            self.timer -= 2
        elif self.state == 2 and self.timer > 3:
            director.change_scene("MainMenuScene")

    def render(self, surface):
        surface.fill((27, 12, 31))
        
        # fade in logo
        if self.state == 0:
            logo = self.logo.copy()

            progress = self.timer / 2

            logo.set_alpha(progress * 255)
            logo.fill(colors.white, special_flags=pygame.BLEND_RGB_ADD)

            surface.blit(logo, logo.get_rect(center=surface.get_rect().center))
        # fade in text as logo moves to top left corner
        elif self.state == 1:
            logo = self.logo.copy()
            logo.fill(colors.white, special_flags=pygame.BLEND_RGB_ADD)

            progress = self.timer / 2
            
            surfaceRect = surface.get_rect()
            surface.blit(logo, logo.get_rect(center=surfaceRect.center))

            text = self.text.copy()
            text.set_alpha(progress * 255)

            textRect = text.get_rect()
            textRect.center = surfaceRect.center
            surface.blit(text, textRect)

            extra = self.extra.copy()
            extra.fill(colors.white, special_flags=pygame.BLEND_RGB_ADD)
            extra.set_alpha(progress * 255)

            extraRect = extra.get_rect()
            extraRect.center = surfaceRect.center
            surface.blit(extra, extraRect)
        # fade logo into color
        elif self.state == 2:
            logo = self.logo.copy()

            progress = self.timer / 2

            surfaceRect = surface.get_rect()

            colorChannel = max(0, 255 - (progress * 255))
            color = (colorChannel, colorChannel, colorChannel)

            logo.fill(color, special_flags=pygame.BLEND_RGB_ADD)
            surface.blit(logo, logo.get_rect(center=surfaceRect.center))

            text = self.text.copy()

            textRect = text.get_rect()
            textRect.center = surfaceRect.center
            surface.blit(text, textRect)

            extra = self.extra.copy()
            extra.fill(color, special_flags=pygame.BLEND_RGB_ADD)

            extraRect = extra.get_rect()
            extraRect.center = surfaceRect.center
            surface.blit(extra, extraRect)