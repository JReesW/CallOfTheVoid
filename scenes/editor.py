import pygame
import json

from engine.scene import Scene
from engine import colors, director, image
from engine.util import get_path

from game.level import load_level
#from scenes.game import GameScene


class EditorScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level = load_level("test")

        self.mouse = (0, 0)
        self.mousedown = 0
        self.highlighted = (0, 0)
        self.last_highlighted = None

        self.tiles = list(self.level.spritesheet.sprites.keys())
        self.tiles_gray = [
            image.recolor(pygame.transform.scale(self.level.spritesheet.get_sprite(sprite), (80, 80)), colors.gray)
            for sprite in self.tiles
        ]
        self.tiles_large = [
            pygame.transform.scale(self.level.spritesheet.get_sprite(sprite), (120, 120))
            for sprite in self.tiles
        ]
        self.tiles_index = 0
        self.selecting_tiles = False

        self.veil = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        self.veil.fill((0, 0, 0, 40))
    
    def handle_events(self, events):
        self.mouse = pygame.mouse.get_pos()

        #keys = pygame.key.get_pressed()

        # if keys[pygame.K_LCTRL] and keys[pygame.K_LSHIFT] and keys[pygame.K_s]:
        #     director.change_scene(GameScene)
        #     return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    self.selecting_tiles = True
                elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                    self.save_level()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.selecting_tiles = False    
            elif event.type == pygame.MOUSEWHEEL:
                self.tiles_index = (self.tiles_index - event.y) % len(self.tiles)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mousedown = 1
                elif event.button == 3:
                    self.mousedown = 3
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in {1, 3}:
                    self.mousedown = 0

    def update(self, dt):
        x, y = self.mouse
        x = x // 48
        y = (y + 12) // 48
        self.highlighted = (x, y)

        if self.mousedown != 0:
            if self.highlighted != self.last_highlighted:
                x, y = self.highlighted
                self.level.tilemap[y][x] = self.tiles[self.tiles_index] if self.mousedown == 1 else ""
                self.level.redraw()

    def render(self, surface):
        surface.fill(colors.grey)

        surface.blit(self.level.surface, (0, 0))
        
        x, y = self.highlighted
        pygame.draw.rect(surface, colors.red, (x*48, y*48 - 12, 48, 48), 2)

        if self.selecting_tiles:
            surface.blit(self.veil, (0, 0))

            pygame.draw.rect(surface, colors.lime, pygame.Rect(900, 480, 120, 120), 2)
            surface.blit(self.tiles_large[self.tiles_index], pygame.Rect(900, 480, 120, 120))
            pygame.draw.rect(surface, colors.lime, pygame.Rect(920, 300, 80, 80), 2)
            surface.blit(self.tiles_gray[(self.tiles_index-1) % len(self.tiles)], pygame.Rect(920, 300, 80, 80))
            pygame.draw.rect(surface, colors.lime, pygame.Rect(920, 700, 80, 80), 2)
            surface.blit(self.tiles_gray[(self.tiles_index+1) % len(self.tiles)], pygame.Rect(920, 700, 80, 80))
    
    def save_level(self):
        level = {
            "spritesheet": "cave",
            "tilemap": self.level.tilemap
        }
        with open(get_path(f"resources/levels/test.json"), 'w') as f:
            json.dump(level, f)
