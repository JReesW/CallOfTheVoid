import pygame
from engine.scene import Scene
from engine import colors, director
from game.earlyCaveSelectPage import EarlyCaveSelectPage
from game.middleCaveSelectPage import MiddleCaveSelectPage
from game.lateCaveSelectPage import LateCaveSelectPage
from game import saveSystem

class LevelSelectScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        director.audio.play_music("level-select")
        if director.level_select is None: director.level_select = self

        saveSystem.load_save_data()

        self.pages = [EarlyCaveSelectPage(), MiddleCaveSelectPage(), LateCaveSelectPage()]
        self.current_page = 0

    def handle_events(self, events):
        self.pages[self.current_page].handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    director.change_scene("MainMenuScene")

    def update(self, dt):
        currentPage = self.pages[self.current_page]
        shouldSwitch, direction = currentPage.should_switch_page()
        if shouldSwitch:
            nextPage = max(0, min(self.current_page + direction, len(self.pages) - 1))
            if nextPage != self.current_page:
                self.current_page = nextPage
                self.pages[self.current_page].selected_node = 0 if direction > 0 else len(self.pages[self.current_page].nodes) - 1
            else:
                currentPage.selected_node -= direction

    def render(self, surface):
        surface.fill(colors.light_sky_blue)
        self.pages[self.current_page].render(surface)