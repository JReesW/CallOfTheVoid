import pygame
import json

from engine.scene import Scene
from engine import colors, director, image, text, mouse, maths
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
        self.elements = ["ladder", "box", "button_off", "plate_off", "gate"]
        self.elements_index = 0
        self.elements_gray = [image.recolor(pygame.transform.scale(image.load_image(element), (80, 80)), colors.gray) for element in self.elements]
        self.elements_large = [pygame.transform.scale(image.load_image(element), (120, 120)) for element in self.elements]
    
        # Links
        self.show_links = False
        self.selecting_links = 0
        self.link_selector = pygame.Rect(1500, 480, 120, 120)
        self.start_link = None

    def handle_events(self, events):
        self.mouse = mouse.mousepos()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and not (self.selecting_start or self.selecting_end or self.selecting_links):
                    self.selecting_tiles = True
                elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                    self.save_level()
                elif event.key == pygame.K_p and (event.mod & pygame.KMOD_CTRL):
                    self.play_level()
                elif event.key == pygame.K_l and (event.mod & pygame.KMOD_CTRL):
                    self.show_links = not self.show_links
                elif event.key == pygame.K_ESCAPE and (self.selecting_start or self.selecting_end or self.selecting_links):
                    self.selecting_start = False
                    self.selecting_end = False
                    self.selecting_links = 0
                    self.start_link = None
                elif event.key == pygame.K_r and not (self.selecting_start or self.selecting_end):
                    if self.selecting_elements and self.elements[self.elements_index] == "gate":
                        self.rotate_gate()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.selecting_tiles = False    
            elif event.type == pygame.MOUSEWHEEL:
                if self.selecting_tiles:
                    if self.selecting_elements:
                        self.elements_index = (self.elements_index - event.y) % len(self.elements)
                    else:
                        self.tiles_index = (self.tiles_index - event.y) % len(self.tiles)
                elif self.selecting_elements and self.elements[self.elements_index] == "gate" and not (self.selecting_start or self.selecting_end):
                    self.change_gate_length(event.y)
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
                    elif self.link_selector.collidepoint(self.mouse):
                        self.selecting_links = 1
                        self.selecting_tiles = False
                elif self.selecting_links > 0:
                    self.lay_links()
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
            if not self.selecting_start and not self.selecting_end and not self.selecting_links:
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
        surface.fill(colors.dark_gray)

        surface.blit(self.level.surface, (0, 0))

        # Gate information
        for x, y, r, l in self.level.gates:
            cx, cy = (x * 48 + 24, y * 48 + 12)
            if r % 2 == 0:
                ly = cy + (-20 if r == 2 else 20)
                dy = (l * 48 - 10) * (1 if r == 2 else -1)
                pygame.draw.line(surface, colors.black, (cx-20, ly), (cx+20, ly), 4)
                pygame.draw.line(surface, colors.black, (cx-15, ly+dy), (cx+15, ly+dy), 3)
                pygame.draw.line(surface, colors.black, (cx, ly), (cx, ly + dy), 2)
            else:
                lx = cx + (-20 if r == 3 else 20)
                dx = (l * 48 - 10) * (1 if r == 3 else -1)
                pygame.draw.line(surface, colors.black, (lx, cy-20), (lx, cy+20), 4)
                pygame.draw.line(surface, colors.black, (lx+dx, cy-15), (lx+dx, cy+15), 3)
                pygame.draw.line(surface, colors.black, (lx, cy), (lx + dx, cy), 2)
        
        # Links
        if self.show_links:
            for x1, y1, x2, y2 in self.level.links:
                cx1, cy1 = (x1 * 48 + 24, y1 * 48 + 12)
                cx2, cy2 = (x2 * 48 + 24, y2 * 48 + 12)
                pygame.draw.line(surface, colors.pink, (cx1, cy1), (cx2, cy2), 2)
                pygame.draw.rect(surface, colors.pink, (cx2-4, cy2-4, 8, 8))
        
        # Tile highlighter
        if not self.selecting_tiles:
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

            # Links selector
            pygame.draw.rect(surface, colors.pink, self.link_selector, 2)
            surface.blit(self.images["link"], self.images["link"].get_rect().move_to(center=self.link_selector.center))
        
        # Placing start/end door
        if self.selecting_start or self.selecting_end:
            x, y = self.mouse
            x = (x // 48) - 1
            y = ((y + 12) // 48) - 1
            x, y = x * 48, y * 48 - 12
            surface.blit(self.images["tp_door"], pygame.Rect(x, y, 144, 144))
        
        # Laying links
        if self.selecting_links == 1:
            for button in [*self.level.buttons, *self.level.plates]:
                x = button[0] * 48
                y = button[1] * 48 - 12
                pygame.draw.rect(surface, colors.cyan, (x, y, 48, 48), 2)
        elif self.selecting_links == 2:
            for gate in self.level.gates:
                x = gate[0] * 48
                y = gate[1] * 48 - 12
                pygame.draw.rect(surface, colors.cyan, (x, y, 48, 48), 2)

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

        # Start/End setting, links setting
        self.images["start"], _ = text.render("S", colors.lime, "Arial", 120, True)
        self.images["end"],   _ = text.render("E", colors.lime, "Arial", 120, True)
        self.images["link"],   _ = text.render("L", colors.pink, "Arial", 120, True)
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
        if element == "gate":
            gates = {(gx, gy): (gr, gl) for gx, gy, gr, gl in self.level.gates}
            if m == 1 and (x, y) not in gates:
                self.level.gates.append([x, y, 0, 2])
                self.changes_made = True
            elif m == 3 and (x, y) in gates:
                self.level.gates.remove([x, y, *gates[(x, y)]])
                self.changes_made = True
                self.check_link_removal("gate", x, y)
        else:
            container = {
                "ladder": self.level.ladders,
                "box": self.level.boxes,
                "button_off": self.level.buttons,
                "plate_off": self.level.plates
            }[element]
            if m == 1 and [x, y] not in container:
                container.append([x, y])
                self.changes_made = True
            elif m == 3 and [x, y] in container:
                container.remove([x, y])
                self.changes_made = True
                self.check_link_removal(element, x, y)


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
            "buttons": self.level.buttons,
            "gates": self.level.gates,
            "plates": self.level.plates,
            "links": self.level.links
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
    
    def rotate_gate(self):
        """
        When in gate-placing-mode, rotate a gate on an R-press
        """
        gates = {(gx, gy): (gr, gl) for gx, gy, gr, gl in self.level.gates}
        x, y, _ = self.highlighted

        if (x, y) in gates:
            r, l = gates[(x, y)]
            self.level.gates.remove([x, y, r, l])
            self.level.gates.append([x, y, (r-1)%4, l])
            self.changes_made = True
    
    def change_gate_length(self, dl):
        """
        When in gate-placing-mode, change a gate's length on a scroll
        """
        gates = {(gx, gy): (gr, gl) for gx, gy, gr, gl in self.level.gates}
        x, y, _ = self.highlighted

        if (x, y) in gates:
            r, l = gates[(x, y)]
            self.level.gates.remove([x, y, r, l])
            self.level.gates.append([x, y, r, maths.clamp(l + dl, 2, 8)])
            self.changes_made = True
    
    def lay_links(self):
        """
        Handle laying links between buttons and gates
        """
        if self.selecting_links == 1:
            for button in [*self.level.buttons, *self.level.plates]:
                x = button[0] * 48
                y = button[1] * 48 - 12
                if pygame.Rect(x, y, 48, 48).collidepoint(self.mouse):
                    self.start_link = button
                    self.selecting_links = 2
        elif self.selecting_links == 2:
            for gate in self.level.gates:
                x = gate[0] * 48
                y = gate[1] * 48 - 12
                if pygame.Rect(x, y, 48, 48).collidepoint(self.mouse):
                    self.level.links.append([*self.start_link, gate[0], gate[1]])
                    self.selecting_links = 0
                    self.changes_made = True

    def check_link_removal(self, element, x, y):
        """
        Check whether to remove a link once one of its elements has been removed
        """
        if element in ["button_off", "plate_off"]:
            self.level.links = [[a, b, c, d] for a, b, c, d in self.level.links if (a, b) != (x, y)]
        elif element == "gate":
            self.level.links = [[a, b, c, d] for a, b, c, d in self.level.links if (c, d) != (x, y)]
