import pygame
import pygame.freetype
from engine.scene import Scene
from engine import colors, director, mouse
from game import saveSystem

import random

class SettingsScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        saveSystem.load_save_data()

        centerx = 1920/2

        self.soundRect = pygame.Rect(100, 100, 500, 100)
        self.soundRect.centerx = centerx
        self.soundVolume = saveSystem.saveData["soundVolume"]
        self.editingSound = False

        self.musicRect = pygame.Rect(100, 230, 500, 100)
        self.musicRect.centerx = centerx
        self.musicVolume = saveSystem.saveData["musicVolume"]
        self.editingMusic = False

        self.deleteDataRect = pygame.Rect(100, 900, 500, 100)
        self.deleteDataRect.centerx = centerx
        self.confirmingDelete = False

        self.mouse = (0, 0)

        self.snowPoints = []

        for i in range(200):
            x = random.randint(0, 1920)
            y = random.randint(0, 1080)
            downwardsForce = random.uniform(1, 5)
            self.snowPoints.append(((x, y), downwardsForce))

    def is_in_rect(self, rect : pygame.Rect, pos):
        return (rect.x + rect.w > pos[0]) and (rect.x < pos[0]) and (rect.y + rect.h > pos[1]) and (rect.y < pos[1])
    
    def updateSoundVolume(self):
        self.soundVolume = max(0, min(1, (self.mouse[0] - self.soundRect.left) / (self.soundRect.right - self.soundRect.left)))
        saveSystem.saveData["soundVolume"] = self.soundVolume
        saveSystem.save_save_data(saveSystem.saveData)
    
    def updateMusicVolume(self):
        self.musicVolume = max(0, min(1, (self.mouse[0] - self.musicRect.left) / (self.musicRect.right - self.musicRect.left)))
        saveSystem.saveData["musicVolume"] = self.musicVolume
        saveSystem.save_save_data(saveSystem.saveData)
    
    def resetSettings(self):
        self.soundVolume = saveSystem.saveData["soundVolume"]
        self.musicVolume = saveSystem.saveData["musicVolume"]

    def handle_events(self, events):
        self.mouse = mouse.mousepos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_in_rect(self.soundRect, self.mouse) and abs(self.mouse[1] - self.soundRect.centery) < 5:
                    self.editingSound = True
                    self.updateSoundVolume()
                if self.is_in_rect(self.musicRect, self.mouse) and abs(self.mouse[1] - self.musicRect.centery) < 5:
                    self.editingMusic = True
                    self.updateMusicVolume()
                
                inDelete = self.is_in_rect(self.deleteDataRect, self.mouse)
                if inDelete:
                    if self.confirmingDelete:
                        saveSystem.save_save_data(saveSystem.defaultData)
                        self.resetSettings()
                        self.confirmingDelete = False
                    else:
                        self.confirmingDelete = True
                else:
                    self.confirmingDelete = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.editingSound = False
                self.editingMusic = False
            elif event.type == pygame.MOUSEMOTION:
                if self.editingSound:
                    self.updateSoundVolume()
                if self.editingMusic:
                    self.updateMusicVolume()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    director.change_scene("MainMenuScene")
    
    def update(self, dt):
        for i in range(len(self.snowPoints)):
            pos, downwardsForce = self.snowPoints[i]
            x = pos[0]
            if x > 1920:
                x = -5
            if pos[1] > 1080:
                pos = (pos[0], -5)
            self.snowPoints[i] = ((x + 2.5, pos[1] + downwardsForce), downwardsForce)
    
    def render(self, surface):
        surface.fill(colors.royal_blue)

        font = pygame.freetype.SysFont("Arial", 26)

        soundTitleSurface, soundTitleRect = font.render("Sound Volume", colors.white)

        soundTitleRect.centerx = self.soundRect.centerx
        soundTitleRect.top = self.soundRect.top

        #light_grey
        backgroundColor = (211, 211, 211, 255)

        backgroundRect = pygame.Rect(self.soundRect)
        backgroundRect.width += 130
        backgroundRect.centery = self.soundRect.centery
        backgroundRect.right = self.soundRect.right + 50

        pygame.draw.rect(surface, backgroundColor, backgroundRect)

        surface.blit(soundTitleSurface, soundTitleRect)

        pygame.draw.line(surface, colors.gray, self.soundRect.midleft, self.soundRect.midright, 5)

        circleX = pygame.math.lerp(self.soundRect.left, self.soundRect.right, self.soundVolume)

        pygame.draw.circle(surface, colors.white_smoke, (circleX, self.soundRect.centery), 5)
        pygame.draw.circle(surface, colors.slate_gray, (circleX, self.soundRect.centery), 3)

        soundVolumeTextSurface, soundVolumeTextRect = font.render(f"{self.soundVolume:.0%}", colors.white)

        soundVolumeTextRect.right = self.soundRect.left - 10
        soundVolumeTextRect.centery = self.soundRect.centery

        surface.blit(soundVolumeTextSurface, soundVolumeTextRect)

        #music
        musicTitleSurface, musicTitleRect = font.render("Music Volume", colors.white)

        musicTitleRect.centerx = self.musicRect.centerx
        musicTitleRect.top = self.musicRect.top

        #light_grey
        backgroundColor = (211, 211, 211, 255)

        backgroundRect = pygame.Rect(self.musicRect)
        backgroundRect.width += 130
        backgroundRect.centery = self.musicRect.centery
        backgroundRect.right = self.musicRect.right + 50

        pygame.draw.rect(surface, backgroundColor, backgroundRect)

        surface.blit(musicTitleSurface, musicTitleRect)

        pygame.draw.line(surface, colors.gray, self.musicRect.midleft, self.musicRect.midright, 5)

        circleX = pygame.math.lerp(self.musicRect.left, self.musicRect.right, self.musicVolume)

        pygame.draw.circle(surface, colors.white_smoke, (circleX, self.musicRect.centery), 5)
        pygame.draw.circle(surface, colors.slate_gray, (circleX, self.musicRect.centery), 3)

        musicVolumeTextSurface, musicVolumeTextRect = font.render(f"{self.musicVolume:.0%}", colors.white)

        musicVolumeTextRect.right = self.musicRect.left - 10
        musicVolumeTextRect.centery = self.musicRect.centery

        surface.blit(musicVolumeTextSurface, musicVolumeTextRect)

        #delete data
        deleteText = "Delete All Data?" if not self.confirmingDelete else "Are You Sure?"

        deleteTextSurface, deleteTextRect = font.render(deleteText, colors.white)
        deleteTextRect.center = self.deleteDataRect.center

        pygame.draw.rect(surface, colors.red, self.deleteDataRect)
        surface.blit(deleteTextSurface, deleteTextRect)

        #snow
        for i in range(len(self.snowPoints)):
            pos, downwardsForce = self.snowPoints[i]
            alpha = 255 - max(0, min(1, (pos[1] / 1080))) * 255
            #colors.snow
            color = (255, 250, 250, alpha)

            pygame.draw.circle(surface, color, pos, 2)