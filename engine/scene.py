import pygame

from engine.maths import clamp


class Camera:
    """
    Controls relative positioning and scaling of all visualised objects
    """

    def __init__(self, pos, screen_size: tuple[int, int] = None, x_bounds: tuple[float, float] = None, y_bounds: tuple[float, float] = None):
        screen_size = pygame.display.get_surface().get_size() if screen_size is None else screen_size
        self.rect = pygame.Rect(*pos, *screen_size)
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds

    def set_center(self, pos: tuple[float, float]):
        """
        Set the center of the camera to the given coords
        """
        top = pos[0] - self.screen_size[0] / 2
        left = pos[1] - self.screen_size[1] / 2
        self.pos = top, left

    def move(self, dx: int, dy: int):
        """
        Move the camera by the given amount of pixels
        :param dx: the change in pixels along the x-axis
        :param dy: the change in pixels along the y-axis
        """
        nx = self.rect.left + dx
        ny = self.rect.top + dy
        if self.x_bounds is not None: nx = clamp(nx, *self.x_bounds)
        if self.y_bounds is not None: ny = clamp(ny, *self.y_bounds)

        self.rect.topleft = nx, ny

    def to_screen_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        """
        Translate a given world position to a screen position
        :param pos: A world position
        :return: A screen position
        """
        x, y = pos
        newpos = (x - self.rect.left), (y - self.rect.top)
        return newpos

    def to_world_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        """
        Translate a given screen position to a world position
        :param pos: A screen position
        :return: A world position
        """
        x, y = pos
        newpos = (x + self.rect.left), (y + self.rect.top)
        return newpos

    def can_see(self, rect: pygame.Rect) -> bool:
        """
        Return whether a given rect falls within the view of the camera
        :param rect: A rectangle
        :return: A boolean
        """
        return self.rect.colliderect(rect)

    def __str__(self):
        return f"Camera<{self.rect.topleft} | {self.screen_size[0]}x{self.screen_size[1]}>"


class Scene:
    def __init__(self, *args, **kwargs):
        self.camera = Camera((0, 0))

    def handle_events(self, events: list[pygame.Event]):
        """
        Handles the given list of pygame events
        """
        pass

    def update(self, dt: float):
        """
        Update the state
        """
        pass

    def render(self, surface: pygame.Surface):
        """
        Render everything to the given surface
        """
        pass
