import pygame

from engine.scene import Scene
from engine import image, director

from scenes.credits import Credits


class Completed(Scene):
    def __init__(self, *args, **kwargs):
        director.audio.play_music("credits")
        self.timer = 420
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                self.timer = 0

    def update(self, dt):
        self.timer -= 1
        if self.timer < 0:
            director.change_scene("Fadeout", self, Credits(keep_music=True))
    
    def render(self, surface):
        surface.blit(image.load_image("the_end"))
