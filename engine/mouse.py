import pygame
from math import hypot


DOUBLE_CLICK_MS = 400
DOUBLE_CLICK_DIST = 8  # pixels

last_click_time = 0
last_click_pos = None


def double_clicked(events: list[pygame.event.Event]):
    """
    Detect a double-click
    """
    global last_click_pos, last_click_time

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            now = pygame.time.get_ticks()
            pos = event.pos

            if last_click_pos is not None:
                dt = now - last_click_time
                dx = pos[0] - last_click_pos[0]
                dy = pos[1] - last_click_pos[1]
                dist = hypot(dx, dy)

                if dt <= DOUBLE_CLICK_MS and dist <= DOUBLE_CLICK_DIST:
                    last_click_time = 0
                    last_click_pos = None
                    return True

            last_click_time = now
            last_click_pos = pos