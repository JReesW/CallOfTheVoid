import pygame

from engine import director, debug
from engine.scene import Scene
from engine.maths import clamp


class Fadeout(Scene):
    def __init__(self, old: Scene, new: Scene, **kwargs):
        self.old = old
        self.new = new
        self.veil = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        self.time_passed = 0
        self.black = False
        self.t0 = 0
        self.t1 = 0.7
        self.t2 = 1.4
        self.t3 = 2.1
        self.t4 = 2.8
    
    def handle_events(self, events):
        pass

    def update(self, dt):
        self.time_passed += dt / 1000
        debug.debug("time passed", f"{self.time_passed:.2f}")
        if self.time_passed < self.t1:
            alpha = clamp(int(pygame.math.remap(self.t0, self.t1, 0, 255, self.time_passed)), 0, 255)
            self.veil.fill((0, 0, 0, alpha))
        elif self.time_passed < self.t2 and not self.black:
            self.veil.fill((0, 0, 0, 255))
            self.black = True
        elif self.time_passed < self.t3:
            alpha = clamp(int(pygame.math.remap(self.t2, self.t3, 255, 0, self.time_passed)), 0, 255)
            debug.debug("alpha", alpha)
            self.veil.fill((0, 0, 0, alpha))
        else:
            director.next_scene = self.new
    
    def render(self, surface):
        if self.time_passed < self.t1:
            self.old.render(surface)
        elif self.t2 <= self.time_passed < self.t3:
            self.new.render(surface)
        surface.blit(self.veil)
        
