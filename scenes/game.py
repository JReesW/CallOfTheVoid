import pygame

from engine.scene import Scene
from engine import colors, director, image, text

from game.player import Player
from game.gate import Gate
from game.button import Button
from game.plate import Plate
from game.level import load_level, Level
from game.box import Box
from game.smoke import SmokeSystem


class GameScene(Scene):
    def __init__(self, level: str = "test", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.level_name = level
        self.level = load_level(level)
        self.allow_edit = "allow_edit" in kwargs and kwargs["allow_edit"]
        self.show_blocks = False
        self.ticks = 0
        if "keep_music" not in kwargs:
            self.music_timestamp = 0
            director.audio.play_music(f"world{self.level.world}")
        else:
            self.music_timestamp = kwargs["keep_music"]
        [director.audio.load_sound(sound) for sound in ["freeze", "unfreeze", "jump"]]

        self.player = Player(self.level)
        self.shadow = Player(self.level, shadow=True)
        self.frozen = False
        self.veil = pygame.Surface(self.shadow.rect.size, pygame.SRCALPHA)
        self.veil.fill((0, 0, 0, 80))

        self.gates = {(x, y): Gate(self.level, (x, y), r, l, i) for x, y, r, l, i in self.level.gates}

        self.buttons = {(x, y): Button(self.level, (x, y)) for x, y in self.level.buttons}
        self.plates = {(x, y): Plate(self.level, (x, y)) for x, y in self.level.plates}
        self.lay_links()
        for gate in self.gates.values():
            gate.check_change()

        self.boxes = [Box(self.level, start) for start in self.level.boxes]

        self.smoke = SmokeSystem()

        self.title = self.generate_title()
        self.show_title = "keep_music" not in kwargs  # don't think too much about it :^)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and (event.mod & pygame.KMOD_CTRL) and self.allow_edit:
                    director.change_scene("EditorScene", level=self.level_name)
                if event.key == pygame.K_h and (event.mod & pygame.KMOD_CTRL):
                    self.show_blocks = not self.show_blocks
                if event.key == pygame.K_LSHIFT:
                    self.freeze_time()
                if event.key == pygame.K_r:
                    self.restart()
        
        if not self.frozen:
            self.player.handle_events(events)
        else:
            self.shadow.handle_events(events)

    def update(self, dt):
        self.ticks += 1

        if self.show_title:
            if self.ticks < 30:
                alpha = pygame.math.clamp(int(pygame.math.remap(0, 30, 0, 255, self.ticks)), 0, 255)
            elif self.ticks > 150:
                alpha = 0
                self.show_title = False
            elif self.ticks > 120:
                alpha = pygame.math.clamp(int(pygame.math.remap(120, 150, 255, 0, self.ticks)), 0, 255)
            else:
                alpha = 255
            self.title.set_alpha(alpha)

        if not self.frozen:
            blocks = self.level.blocks + [b.rect for b in self.boxes if not b.held] + [g.rect for g in self.gates.values()]
            self.player.update(dt, blocks, self.level.death_blocks)
            if self.player.rect.top > 1080 or self.player.dead:
                self.restart()
            
            for plate in self.plates.values():
                plate.update()

            for gate in self.gates.values():
                gate.update()
            
            for box in sorted(self.boxes, key=lambda b: b.rect.top):
                blocks = self.level.blocks + [b.rect for b in self.boxes if b is not box and not b.held] + [g.rect for g in self.gates.values()] + [p.box_rect for p in self.plates.values()] + self.level.death_blocks
                box.update(dt, blocks)
            
            if self.shadow.leaving_mark and self.ticks % 10 == 0 and not self.shadow.dead:
                self.smoke.emit((self.shadow.rect.centerx, self.shadow.rect.bottom), 1)
        else:
            blocks = self.level.blocks + [g.rect for g in self.gates.values()]
            boxes = [b.rect for b in self.boxes]
            if self.shadow.collides_with_box: blocks += boxes
            self.shadow.update(dt, blocks, self.level.death_blocks, boxes)
            if self.shadow.rect.top > 1280:
                self.shadow.dead = True
                self.shadow.leaving_mark = False
                self.freeze_time()

    def render(self, surface):
        surface.fill(colors.steel_blue)

        surface.blit(self.level.background)

        if not self.frozen:
            for button in self.buttons.values():
                surface.blit(button.image, button.rect)
        else:
            for button in self.buttons.values():
                img = image.load_image("button_shadow_on" if button.pressed else "button_shadow_off")
                director.post.overlay_surf.blit(img, button.rect)
        
        for plate in self.plates.values():
            surface.blit(plate.image, plate.rect)

        for gate in self.gates.values():
            gate.render(surface)

        surface.blit(self.level.surface, (0, 0))

        for box in self.boxes:
            surface.blit(box.image, box.rect)        
        
        self.player.render(surface)

        if self.frozen:
            self.shadow.render(director.post.overlay_surf)
        elif self.shadow.leaving_mark:
            self.smoke.update_draw(surface, 1/60)
        
        self.show_tutorial(surface)

        # Hitbox debug mode (Ctrl + H)
        if self.show_blocks:
            pygame.draw.rect(surface, colors.blue, self.shadow.rect if self.frozen else self.player.rect, 2)
            for block in self.level.blocks:
                pygame.draw.rect(surface, colors.red, block, 2)
            for l_block in self.level.ladder_blocks:
                pygame.draw.rect(surface, colors.yellow, l_block, 2)
            for box in self.boxes:
                pygame.draw.rect(surface, colors.cyan, box.rect, 2)
            for button in self.buttons.values():
                pygame.draw.rect(surface, colors.alice_blue, button.rect, 2)
            for plate in self.plates.values():
                pygame.draw.rect(surface, colors.alice_blue, plate.rect, 2)
            for gate in self.gates.values():
                pygame.draw.rect(surface, colors.orange, gate.rect, 2)
        
        if self.show_title:
            rect = pygame.Rect(0, 0, *self.title.get_size())
            rect.center = (960, 50)
            surface.blit(self.title, rect)
    
    def freeze_time(self):
        """
        Swap between freezing and unfreezing time
        """
        self.frozen = not self.frozen
        director.post.saturation = 0 if self.frozen else 1
        director.post.value = 0.7 if self.frozen else 1
        track = f"world{self.level.world}{'-alt' if self.frozen else ''}"
        self.music_timestamp += pygame.mixer.music.get_pos()/1000
        try:
            director.audio.play_music(track, start=self.music_timestamp)
        except NotImplementedError:
            self.music_timestamp = 0
            director.audio.play_music(track, start=0)
        director.audio.play_sound("freeze" if self.frozen else "unfreeze")

        if self.frozen:
            self.shadow.collides_with_box = False
            if self.level.world < 3 or not self.shadow.leaving_mark or self.shadow.dead:
                self.shadow.dead = False
                self.shadow.rect = self.player.rect.copy()
                self.shadow.velocity = self.player.velocity.copy()
                self.shadow.grounded = self.player.grounded
                self.shadow.looking_left = self.player.looking_left
            director.post.play_shockwave_anim(pygame.Vector2(self.shadow.rect.center))
        else:
            if self.level.world > 1 and self.shadow.looking_down:
                if self.player.grabbed is not None: self.player.drop_box(force=True)
                self.player.rect = self.shadow.rect.copy()
                self.player.velocity = self.shadow.velocity.copy()
                self.player.grounded = self.shadow.grounded
                self.player.looking_left = self.shadow.looking_left
                self.shadow.leaving_mark = False
            elif self.level.world == 3:
                if self.shadow.looking_up:
                    self.shadow.leaving_mark = False
                else:
                    self.shadow.leaving_mark = True
            self.smoke.particles.clear()

    def lay_links(self):
        """
        Lay the links between buttons and gates
        """
        for x1, y1, x2, y2 in self.level.links:
            if (x1, y1) in self.buttons:
                self.buttons[(x1, y1)].outputs.append(self.gates[(x2, y2)])
            else:
                self.plates[(x1, y1)].outputs.append(self.gates[(x2, y2)])
            self.gates[(x2, y2)].inputs[(x1, y1)] = False
    
    def restart(self):
        """
        Restart the level
        """
        director.change_scene("Fadeout", self, GameScene(self.level_name, keep_music=self.music_timestamp, allow_edit=self.allow_edit))

    def generate_title(self) -> pygame.Surface:
        """
        Generate a title for the level name, shown when starting a level
        """
        surf, rect = text.render(self.level.name, colors.black, "Arial", 48, True)
        title_rect = pygame.Rect(0, 0, max(rect.width + 20, 200), rect.height + 20)
        surface = pygame.Surface(title_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, colors.white, title_rect, border_radius=10)
        pygame.draw.rect(surface, colors.black, title_rect, 4, border_radius=10)
        rect.center = title_rect.center
        surface.blit(surf, rect)
        return surface

    def show_tutorial(self, surface: pygame.Surface):
        """
        Show a tutorial image
        """
        name = self.level.name.lower()
        if name == "cave entrance":
            surface.blit(image.load_image("tutorials/jump"), (630, 330))
            surface.blit(image.load_image("tutorials/move"), (1240, 880))
        elif self.level.name.lower() == "mind the gap":
            surface.blit(image.load_image("tutorials/toggle_button"), (100, 100))
            surface.blit(image.load_image("tutorials/freeze_time"), (650, 200))
