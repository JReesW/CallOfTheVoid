import sys
import pygame

from engine import debug, director

pygame.init()
pygame.freetype.init()


screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Pygame project")

FPS = 60
clock = pygame.time.Clock()
running = True

director.find_scenes()
director.change_scene("EditorScene")
director._set_scene()

while running:
    dt = clock.tick(FPS)

    surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q and (event.mod & pygame.KMOD_CTRL)):
            pygame.quit()
            sys.exit()

    # Call the necessary scene functions of the active scene
    director.scene.handle_events(events)
    director.scene.update(dt)
    director.scene.render(surface)

    if director.next_scene is not None:
        director._set_scene()

    if debug.is_active():
        debug.render(surface)

    screen.blit(surface, (0, 0))

    # Draw the surface to the screen
    pygame.display.flip()
