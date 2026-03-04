import pygame
from engine.scene import Scene
from engine import colors, director
from game.player import Player
from game.gate import Gate
from game.button import Button
from game.level import load_level


class GameScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level = load_level("test")
        self.allow_edit = "allow_edit" in kwargs and kwargs["allow_edit"]
        self.show_blocks = False

        self.player = Player(self.level.start)

        self.gates = []
        # self.gates.append(Gate(size=(100, 200), position=(800, 400), buttonCount=2))

        self.buttons = []
        # self.buttons.append(Button(size=(50, 50), position=(425, 550), gates=[self.gates[0]]))
        # self.buttons.append(Button(size=(50, 50), position=(600, 550), gates=[self.gates[0]]))
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and (event.mod & pygame.KMOD_CTRL) and self.allow_edit:
                    director.change_scene("EditorScene")
                if event.key == pygame.K_h and (event.mod & pygame.KMOD_CTRL):
                    self.show_blocks = not self.show_blocks
        
        self.player.handle_events(events)

    def update(self, dt):
        self.player.update(dt, self.level.blocks + [gate.rect for gate in self.gates if not gate.open])

        for button in self.buttons:
            button.collide([self.player])
        
        for gate in self.gates:
            gate.update(dt)

    def render(self, surface):
        surface.fill(colors.black)

        surface.blit(self.level.surface, (0, 0))
        
        for gate in self.gates:
            gate.render(surface)
        
        for button in self.buttons:
            button.render(surface)
        
        self.player.render(surface)

        if self.show_blocks:
            for block in self.level.blocks:
                pygame.draw.rect(surface, colors.red, block, 2)
