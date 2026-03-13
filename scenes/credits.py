import pygame

from engine.scene import Scene
from engine import image, director


class Credits(Scene):
    def __init__(self, keep_music: bool = False, *args, **kwargs):
        if not keep_music:
            director.audio.play_music("credits")
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                director.change_scene("MainMenuScene")

    def update(self, dt):
        pass
        
    def render(self, surface):
        surface.blit(image.load_image("credits"))
