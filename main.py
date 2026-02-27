import sys
from pathlib import Path
import pygame

from engine import debug, director, postprocessing
from scenes.game import GameScene

pygame.init()
pygame.freetype.init()


screen = pygame.display.set_mode(
    (1920, 1080),
    pygame.FULLSCREEN | pygame.OPENGL | pygame.DOUBLEBUF
)
pygame.display.set_caption("Pygame project")

post = postprocessing.PostProcessing(
    (1920, 1080),
    str((Path.cwd() / "resources" / "shaders" / "postprocessing.glsl").absolute())
)

FPS = 60
clock = pygame.time.Clock()
running = True

director.change_scene(GameScene)
director._set_scene()

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

    if director.next_scene is not None:
        director._set_scene()

    if debug.is_active():
        debug.render(surface)

    screen.blit(surface, (0, 0))

    mouse = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (255, 255, 0), mouse, 15, 0)

    post.upload(screen)
    post.render()

    # Draw the surface to the screen
    pygame.display.flip()
