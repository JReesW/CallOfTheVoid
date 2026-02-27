import pygame
from engine.scene import Scene


class GameScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        pass
