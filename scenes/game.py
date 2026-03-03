import pygame
from engine.scene import Scene
from engine import colors
from game.block import Block
from game.player import Player
from game.level import load_level


class GameScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level = load_level("test")

        self.player = Player()
        self.player.position = pygame.math.Vector2(500, 500)

        self.blocks = []
        self.blocks.append(Block(size=(100, 20), position=(500, 600)))
        self.blocks.append(Block(size=(20, 100), position=(600, 500)))
    
    def handle_events(self, events):
        self.player.handle_events(events)

    def update(self, dt):
        self.player.update(dt, self.blocks)

    def render(self, surface):
        surface.fill(colors.black)

        surface.blit(self.level.surface, (0, 0))

        self.player.render(surface)

        for block in self.blocks:
            block.render(surface)
