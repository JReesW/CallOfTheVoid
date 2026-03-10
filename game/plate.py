import pygame

from engine import image, director
from game.level import Level


class Plate(pygame.sprite.Sprite):
    def __init__(self, level: Level, start: tuple[int, int], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level = level
        self.image = image.load_image("plate_off")
        self.rect = pygame.FRect(start[0] * 48, start[1] * 48, 48, 48)
        self.trigger_rect = pygame.FRect(start[0] * 48, start[1] * 48 + 24, 48, 24)
        self.box_rect = pygame.FRect(start[0] * 48, start[1] * 48 + 36, 48, 12)

        self.start = start
        self.pressed = False
        self.now_pressed = False
        self.outputs = []
    
    def update(self):
        rects = [box.rect for box in director.scene.boxes] + [director.scene.player.rect]
        for rect in rects:
            if self.trigger_rect.colliderect(rect):
                self.now_pressed = True
                break
        else:
            self.now_pressed = False
        
        if self.pressed != self.now_pressed:
            self.pressed = self.now_pressed
            self.toggle()
    
    def toggle(self):
        self.image = image.load_image("plate_on") if self.pressed else image.load_image("plate_off")
        for output in self.outputs:
            output.inputs[self.start] = self.pressed
            output.check_change()