import pygame
import json

from engine.scene import Scene
from engine import colors, director, image, text, mouse
from engine.util import get_path

from game.level import load_level


class EditorScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        director.post.reset()

        self.level = load_level("test", editing=True)

        # Mouse info
        self.mouse = (0, 0)
        self.mousedown = 0
        self.highlighted = (0, 0, 0)
        self.last_highlighted = None

        # Tile picker stuff
        self.tiles = [tile for tile in self.level.spritesheet.sprites.keys() if tile in self.level.solid]
        self.tiles_gray = [image.recolor(pygame.transform.scale(self.level.spritesheet.get_sprite(sprite), (80, 80)), colors.gray) for sprite in self.tiles]
        self.tiles_large = [pygame.transform.scale(self.level.spritesheet.get_sprite(sprite), (120, 120)) for sprite in self.tiles]
        self.tiles_index = 0
        self.selecting_tiles = False

        # Grey overlay for the tile picker
        self.veil = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        self.veil.fill((0, 0, 0, 40))

        # Keep track of whether the level must be saved to store changes made
        self.changes_made = False
        self.changes_warning = 0

        # Some pregenerated images
        self.images: dict[str, pygame.Surface] = {}
        self.generate_images()

        # More editor tools
        self.selecting_start = False
        self.selecting_end = False
        self.start_selector = pygame.Rect(300, 400, 120, 120)
        self.end_selector = pygame.Rect(300, 560, 120, 120)
        
        # Tiles/Elements tabs
        self.selecting_elements = False
        self.tiles_tab = pygame.Rect(689, 100, 270, 55)
        self.elements_tab = pygame.Rect(960, 100, 270, 55)

        # Elements picker
        self.elements = ["ladder", "box", "button_off"]
        self.elements_index = 0
        self.elements_gray = [image.recolor(pygame.transform.scale(image.load_image(element), (80, 80)), colors.gray) for element in self.elements]
        self.elements_large = [pygame.transform.scale(image.load_image(element), (120, 120)) for element in self.elements]
    
    def handle_events(self, events):
        self.mouse = mouse.mousepos()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and not (self.selecting_start or self.selecting_end):
                    self.selecting_tiles = True
                elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                    self.save_level()
                elif event.key == pygame.K_p and (event.mod & pygame.KMOD_CTRL):
                    self.play_level()
                elif event.key == pygame.K_ESCAPE and (self.selecting_start or self.selecting_end):
                    self.selecting_start = False
                    self.selecting_end = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.selecting_tiles = False    
            elif event.type == pygame.MOUSEWHEEL:
                if self.selecting_elements:
                    self.elements_index = (self.elements_index - event.y) % len(self.elements)
                else:
                    self.tiles_index = (self.tiles_index - event.y) % len(self.tiles)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.selecting_tiles:
                    if self.start_selector.collidepoint(self.mouse):
                        self.selecting_start = True
                        self.selecting_tiles = False
                    elif self.end_selector.collidepoint(self.mouse):
                        self.selecting_end = True
                        self.selecting_tiles = False
                    elif self.tiles_tab.collidepoint(self.mouse):
                        self.selecting_elements = False
                    elif self.elements_tab.collidepoint(self.mouse):
                        self.selecting_elements = True
                else:
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
        self.highlighted = (x, y, self.mousedown)

        if self.mousedown != 0 and not self.selecting_tiles:
            if not self.selecting_start and not self.selecting_end:
                if self.highlighted != self.last_highlighted:
                    self.last_highlighted = self.highlighted
                    x, y, m = self.highlighted
                    if self.selecting_elements:
                        self.place_element(x, y, m)
                    else:
                        if self.level.tilemap[y][x] != (self.tiles[self.tiles_index] if self.mousedown == 1 else ""):
                            self.changes_made = True
                        self.level.tilemap[y][x] = self.tiles[self.tiles_index] if self.mousedown == 1 else ""
                    self.level.redraw()
            else:
                if self.selecting_start:
                    self.level.start = self.highlighted[:2]
                    self.selecting_start = False
                elif self.selecting_end:
                    self.level.end = self.highlighted[:2]
                    self.selecting_end = False
                self.mousedown = 0
                self.changes_made = True
                self.level.redraw()

        if self.changes_warning > 0:
            self.changes_warning -= 1

    def render(self, surface):
        surface.fill(colors.grey)

        surface.blit(self.level.surface, (0, 0))
        
        # Tile highlighter
        x, y, _ = self.highlighted
        hl_color = colors.lime if self.selecting_start or self.selecting_end else colors.red
        pygame.draw.rect(surface, hl_color, (x*48, y*48 - 12, 48, 48), 2)

        # Tile selector
        if self.selecting_tiles:
            surface.blit(self.veil, (0, 0))

            # Selector "wheel"
            large, gray, index, color, group = (self.elements_large, self.elements_gray, self.elements_index, colors.blue_violet, self.elements) \
                if self.selecting_elements else \
                (self.tiles_large, self.tiles_gray, self.tiles_index, colors.lime, self.tiles)
            pygame.draw.rect(surface, color, pygame.Rect(900, 480, 120, 120), 2)
            surface.blit(large[index], pygame.Rect(900, 480, 120, 120))
            pygame.draw.rect(surface, color, pygame.Rect(920, 300, 80, 80), 2)
            surface.blit(gray[(index-1) % len(group)], pygame.Rect(920, 300, 80, 80))
            pygame.draw.rect(surface, color, pygame.Rect(920, 700, 80, 80), 2)
            surface.blit(gray[(index+1) % len(group)], pygame.Rect(920, 700, 80, 80))

            # Start/end selectors
            pygame.draw.rect(surface, colors.yellow, self.start_selector, 2)
            surface.blit(self.images["start"], self.images["start"].get_rect().move_to(center=self.start_selector.center))
            pygame.draw.rect(surface, colors.yellow, self.end_selector, 2)
            surface.blit(self.images["end"], self.images["end"].get_rect().move_to(center=self.end_selector.center))

            # Tiles/elements selectors
            surface.blit(self.images["tiles_dark" if self.selecting_elements else "tiles"], self.tiles_tab)
            surface.blit(self.images["elements" if self.selecting_elements else "elements_dark"], self.elements_tab)
        
        if self.selecting_start or self.selecting_end:
            x, y = self.mouse
            x = (x // 48) - 1
            y = ((y + 12) // 48) - 1
            x, y = x * 48, y * 48 - 12
            surface.blit(self.images["tp_door"], pygame.Rect(x, y, 144, 144))

        # Show unsaved level warning
        if self.changes_warning > 0:
            rect = pygame.Rect(0, 0, *self.images["unsaved"].get_size())
            rect.bottomright = (1910, 1070)
            surface.blit(self.images["unsaved"], rect)
    
    def generate_images(self):
        """
        Pregenerate some handy images (e.g. error messages)
        """
        # "Save before playing" error message
        surf, rect = text.render("Warning: Save level before playing", colors.maroon, "Arial", 24, True)
        msg_surf = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(msg_surf, colors.red, msg_surf.get_rect())
        pygame.draw.rect(msg_surf, colors.maroon, msg_surf.get_rect(), 5)
        rect.center = msg_surf.get_rect().center
        msg_surf.blit(surf, rect)
        self.images["unsaved"] = msg_surf

        # Start/End setting
        self.images["start"], _ = text.render("S", colors.lime, "Arial", 120, True)
        self.images["end"],   _ = text.render("E", colors.lime, "Arial", 120, True)
        self.images["tp_door"] = self.level.spritesheet.get_sprite("DOOR").copy()
        self.images["tp_door"].set_alpha(60)

        # Tiles/Elements selectors
        def tiles_elements(title, dark):
            color = colors.alter(colors.lime if title == "Tiles" else colors.blue_violet, 0.6 if dark else 1)
            color2 = colors.alter(colors.lime if title == "Tiles" else colors.blue_violet, 0.3 if dark else 0.5)
            surf, rect = text.render(title, color, "Arial", 48)
            _surf = pygame.Surface((270, 55), pygame.SRCALPHA)
            lr, rr = (8, -1) if title == "Tiles" else (-1, 8)
            pygame.draw.rect(_surf, color2, _surf.get_rect(), border_top_left_radius=lr, border_bottom_left_radius=lr, border_top_right_radius=rr, border_bottom_right_radius=rr)
            pygame.draw.rect(_surf, color, _surf.get_rect(), 3, border_top_left_radius=lr, border_bottom_left_radius=lr, border_top_right_radius=rr, border_bottom_right_radius=rr)
            rect.center = _surf.get_rect().center
            _surf.blit(surf, rect)
            return _surf
        
        self.images["tiles"] = tiles_elements("Tiles", False)
        self.images["tiles_dark"] = tiles_elements("Tiles", True)
        self.images["elements"] = tiles_elements("Elements", False)
        self.images["elements_dark"] = tiles_elements("Elements", True)

    def place_element(self, x, y, m):
        """
        Place the currently selected element at the given position
        """
        element = self.elements[self.elements_index]
        container = {
            "ladder": self.level.ladders,
            "box": self.level.boxes,
            "button_off": self.level.buttons
        }[element]
        if m == 1 and [x, y] not in container:
            container.append([x, y])
        elif m == 3 and [x, y] in container:
            container.remove([x, y])


    def save_level(self):
        """
        Save the level to resources/levels/test.json
        """
        level = {
            "spritesheet": "cave",
            "tilemap": self.level.tilemap,
            "solid": self.level.solid,
            "start": self.level.start,
            "end": self.level.end,
            "ladders": self.level.ladders,
            "boxes": self.level.boxes,
            "buttons": self.level.buttons
        }
        with open(get_path(f"resources/levels/test.json"), 'w') as f:
            json.dump(level, f)
        self.changes_made = False
    
    def play_level(self):
        """
        Play the level, given it has been saved
        """
        if self.changes_made:
            self.changes_warning = 300
        else:
            director.change_scene("GameScene", allow_edit=True)
