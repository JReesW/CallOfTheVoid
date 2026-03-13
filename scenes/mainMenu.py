import pygame
import pygame.freetype
import sys
import random
from engine.scene import Scene
from engine import colors, director, mouse, image
from engine.util import get_path

class MainMenuScene(Scene):
    def __init__(self, keep_music: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not keep_music:
            director.audio.play_music("title")

        self.logo = pygame.image.load(get_path(f"resources/images/lowland_palms_splash.png")).convert_alpha()
        self.logoRect = self.logo.get_rect()
        self.logoRect.right = 1920
        self.logoRect.bottom = 1080

        self.pyce = pygame.image.load(get_path(f"resources/images/pygamece_powered_splash.png")).convert_alpha()
        self.pyceRect = self.pyce.get_rect()
        self.pyceRect.left = 0
        self.pyceRect.bottom = 1080

        self.buttons: list[pygame.Rect] = []
        centerx = 1920/2
        #start, settings, credits?, quit
        self.startButton = pygame.Rect((10, 500, 300, 70))
        self.startButton.centerx = centerx
        self.buttons.append(self.startButton)

        self.settingsButton = pygame.Rect((10, 580, 300, 70))
        self.settingsButton.centerx = centerx
        self.buttons.append(self.settingsButton)

        self.creditsButton = pygame.Rect((10, 660, 300, 70))
        self.creditsButton.centerx = centerx
        self.buttons.append(self.creditsButton)

        self.quitButton = pygame.Rect((10, 740, 300, 70))
        self.quitButton.centerx = centerx
        self.buttons.append(self.quitButton)

        self.mouse = (0,0)

        self.snowPoints = []

        for i in range(200):
            x = random.randint(0, 1920)
            y = random.randint(0, 1080)
            downwardsForce = random.uniform(1, 5)
            self.snowPoints.append(((x, y), downwardsForce))

    def handle_events(self, events):
        self.mouse = mouse.mousepos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if self.is_in_rect(button, self.mouse):
                        if button == self.startButton:
                            director.change_scene("LevelSelectScene")
                        elif button == self.settingsButton:
                            director.change_scene("SettingsScene")
                        elif button == self.creditsButton:
                            director.change_scene("Credits")
                        elif button == self.quitButton:
                            pygame.quit()
                            sys.exit()

    def update(self, dt):
        for i in range(len(self.snowPoints)):
            pos, downwardsForce = self.snowPoints[i]
            x = pos[0]
            if x > 1920:
                x = -5
            if pos[1] > 1080:
                pos = (pos[0], -5)
            self.snowPoints[i] = ((x + 2.5, pos[1] + downwardsForce), downwardsForce)
    
    def is_in_rect(self, rect : pygame.Rect, pos):
        return (rect.x + rect.w > pos[0]) and (rect.x < pos[0]) and (rect.y + rect.h > pos[1]) and (rect.y < pos[1])

    def render(self, surface):
        surface.fill((111, 103, 118))

        titleSurface = image.load_image("title")
        rect = pygame.Rect(0, 0, *titleSurface.get_size())
        rect.centerx = surface.width / 2
        rect.top = 200

        surface.blit(titleSurface, rect)

        #pygame.draw.rect(surface, colors.red, self.logoRect)

        surface.blit(self.logo, self.logoRect)

        surface.blit(self.pyce, self.pyceRect)
        
        for button in self.buttons:
            hovered = self.is_in_rect(button, self.mouse)

            if hovered:
                outline = pygame.Surface((button.width + 6, button.height + 6))
                outlineRect = outline.get_rect(center=button.center)

                outline.fill((124, 161, 192))

                surface.blit(outline, outlineRect)

            
            pygame.draw.rect(surface, (65, 106, 163), button)

            if button == self.startButton:
                font = pygame.freetype.SysFont("Arial", 26)
                textSurface, textRect = font.render("Start", colors.white)
                textRect.center = button.center

                surface.blit(textSurface, textRect)
            elif button == self.settingsButton:
                font = pygame.freetype.SysFont("Arial", 26)
                textSurface, textRect = font.render("Settings", colors.white)
                textRect.center = button.center

                surface.blit(textSurface, textRect)
            elif button == self.creditsButton:
                font = pygame.freetype.SysFont("Arial", 26)
                textSurface, textRect = font.render("Credits", colors.white)
                textRect.center = button.center

                surface.blit(textSurface, textRect)
            elif button == self.quitButton:
                font = pygame.freetype.SysFont("Arial", 26)
                textSurface, textRect = font.render("Quit", colors.white)
                textRect.center = button.center

                surface.blit(textSurface, textRect)
        
        for i in range(len(self.snowPoints)):
            pos, downwardsForce = self.snowPoints[i]
            alpha = 255 - max(0, min(1, (pos[1] / 1080))) * 255
            #colors.snow
            color = (255, 250, 250, alpha)

            pygame.draw.circle(surface, color, pos, 2)
