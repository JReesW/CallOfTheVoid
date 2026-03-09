import pygame
import pygame.freetype
import sys
from engine.scene import Scene
from engine import colors, director, mouse

class MainMenuScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buttons: list[pygame.Rect] = []
        #start, settings, credits?, quit
        self.startButton = pygame.Rect((10, 760, 300, 70))
        self.buttons.append(self.startButton)

        self.settingsButton = pygame.Rect((10, 840, 300, 70))
        self.buttons.append(self.settingsButton)

        self.creditsButton = pygame.Rect((10, 920, 300, 70))
        self.buttons.append(self.creditsButton)

        self.quitButton = pygame.Rect((10, 1000, 300, 70))
        self.buttons.append(self.quitButton)

        self.mouse = (0,0)

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
                        elif button == self.quitButton:
                            pygame.quit()
                            sys.exit()

    def update(self, dt):
        pass
    
    def is_in_rect(self, rect : pygame.Rect, pos):
        return (rect.x + rect.w > pos[0]) and (rect.x < pos[0]) and (rect.y + rect.h > pos[1]) and (rect.y < pos[1])

    def render(self, surface):
        surface.fill((111, 103, 118))
        
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
