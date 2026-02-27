import sys
import pygame

from engine import debug, director
from scenes.game import GameScene

pygame.init()
pygame.freetype.init()


screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Pygame project")

FPS = 60
clock = pygame.time.Clock()
running = True

director.set_scene(GameScene)

while running:
    dt = clock.tick(FPS)

    surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Call the necessary scene functions of the active scene
    director.scene.handle_events(events)
    director.scene.update(dt)
    director.scene.render(surface)

    if debug.is_active():
        debug.render(surface)

    screen.blit(surface, (0, 0))

    # Draw the surface to the screen
    pygame.display.flip()
