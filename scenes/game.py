import pygame
from engine.scene import Scene
from engine import colors, director
from game.player import Player
from game.gate import Gate
from game.button import Button
from game.level import load_level, Level
from game.box import Box


class GameScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level = load_level("test")
        self.allow_edit = "allow_edit" in kwargs and kwargs["allow_edit"]
        self.show_blocks = False

        self.player = Player(self.level)
        self.shadow = Player(self.level, shadow=True)
        self.frozen = False
        self.frozen_overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        self.frozen_overlay.fill((150, 150, 150))

        self.gates = []
        # self.gates.append(Gate(size=(100, 200), position=(800, 400), buttonCount=2))

        self.buttons = []
        # self.buttons.append(Button(size=(50, 50), position=(425, 550), gates=[self.gates[0]]))
        # self.buttons.append(Button(size=(50, 50), position=(600, 550), gates=[self.gates[0]]))

        self.boxes = [Box(self.level, start) for start in self.level.boxes]
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and (event.mod & pygame.KMOD_CTRL) and self.allow_edit:
                    director.change_scene("EditorScene")
                if event.key == pygame.K_h and (event.mod & pygame.KMOD_CTRL):
                    self.show_blocks = not self.show_blocks
                if event.key == pygame.K_LSHIFT:
                    self.freeze_time()
        
        if not self.frozen:
            self.player.handle_events(events)
        else:
            self.shadow.handle_events(events)

    def update(self, dt):
        blocks = self.level.blocks + [b.rect for b in self.boxes if not b.held]
        if not self.frozen:
            self.player.update(dt, blocks)

            for button in self.buttons:
                button.collide([self.player])
            
            for gate in self.gates:
                gate.update(dt)
            
            for box in sorted(self.boxes, key=lambda b: b.rect.top):
                blocks = self.level.blocks + [b.rect for b in self.boxes if b is not box and not b.held]
                box.update(dt, blocks)
        else:
            self.shadow.update(dt, blocks)

    def render(self, surface):
        surface.fill(colors.steel_blue)

        surface.blit(self.level.surface, (0, 0))
        
        for gate in self.gates:
            gate.render(surface)
        
        for button in self.buttons:
            button.render(surface)

        for box in self.boxes:
            surface.blit(box.image, box.rect)        
        
        self.player.render(surface)

        if self.frozen:
            self.shadow.render(surface)

        # Hitbox debug mode (Ctrl + H)
        if self.show_blocks:
            pygame.draw.rect(surface, colors.blue, self.shadow.rect if self.frozen else self.player.rect, 2)
            for block in self.level.blocks:
                pygame.draw.rect(surface, colors.red, block, 2)
            for l_block in self.level.ladder_blocks:
                pygame.draw.rect(surface, colors.yellow, l_block, 2)
            for box in self.boxes:
                pygame.draw.rect(surface, colors.cyan, box.rect, 2)
    
    def freeze_time(self):
        """
        Swap between freezing and unfreezing time
        """
        self.frozen = not self.frozen
        director.post.saturation = 0 if self.frozen else 1
        director.post.value = 0.5 if self.frozen else 1

        if self.frozen:
            director.post.play_shockwave_anim(pygame.Vector2(self.player.rect.center))
            self.shadow.rect = self.player.rect.copy()
            self.shadow.velocity = self.player.velocity.copy()
            self.shadow.grounded = self.player.grounded
            self.shadow.looking_left = self.player.looking_left
