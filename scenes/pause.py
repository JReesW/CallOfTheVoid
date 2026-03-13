import pygame

from engine.scene import Scene
from engine import director, mouse, text, colors


class Pause(Scene):
    def __init__(self, under: Scene, *args, **kwargs):
        self.under = under
        self.veil = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        self.veil.fill((0, 0, 0, 70))

        self.resume = pygame.Rect(0, 400, 400, 100)
        self.quit = pygame.Rect(0, 530, 400, 100)
        self.resume.centerx = 960
        self.quit.centerx = 960
        self.mouse = (0, 0)

    def handle_events(self, events):
        self.mouse = mouse.mousepos()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                director.next_scene = self.under
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.resume.collidepoint(self.mouse):
                    director.next_scene = self.under
                elif self.quit.collidepoint(self.mouse):
                    director.audio.play_music("level-select")
                    director.next_scene = director.level_select
    
    def update(self, dt):
        pass
    
    def render(self, surface):
        self.under.render(surface)
        surface.blit(self.veil)
        overlay = director.post.overlay_surf

        for i, button in enumerate([self.resume, self.quit]):
            hovered = button.collidepoint(self.mouse)

            if hovered:
                outline = pygame.Surface((button.width + 6, button.height + 6))
                outlineRect = outline.get_rect(center=button.center)
                outline.fill((124, 161, 192))
                overlay.blit(outline, outlineRect)

            pygame.draw.rect(overlay, (65, 106, 163), button)
            txt = ["Resume", "Quit"][i]
            surf, rect = text.render(txt, colors.white, "Arial", 64, True)
            rect.center = button.center
            overlay.blit(surf, rect)