from typing import Any

from array import array
from time import time
from pathlib import Path

import pygame
import moderngl

from engine.util import get_path


class PostProcessing:
    """
    Screen-quad with a texture for post-processing effects.
    """

    def __init__(self,
            resolution: tuple[int, int],
            fragment_path: str,
            suppress_uniform_errors: bool = True
            ) -> None:
        """
        Parameters
        -----------
        resolution
            Screen-quad dimensions
        fragment_path
            Filepath to fragment shader
        suppress_uniform_errors
            Suppress key errors when accessing uniform blocks.

            Should only be used for production with proper logging.
        """

        base_vertex_shader = """
        #version 330

        in vec2 in_position;
        in vec2 in_uv;

        out vec2 v_uv;

        void main() {
            gl_Position = vec4(in_position, 0.0, 1.0);

            v_uv = in_uv;
        }
        """

        self._resolution = resolution
        self._suppress_uniform_errors = suppress_uniform_errors
        self._context = moderngl.get_context()

        self._vbo = self.create_buffer_object([-1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, -1.0])
        self._uvbo = self.create_buffer_object([0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0])
        self._ibo = self.create_buffer_object([0, 1, 2, 1, 2, 3])

        self._program = self._context.program(
            vertex_shader=base_vertex_shader,
            fragment_shader=open(fragment_path, "r", encoding="utf-8").read()
        )
        self.reset()

        self._vao = self._context.vertex_array(
            self._program,
            (
                (self._vbo, "2f", "in_position"),
                (self._uvbo, "2f", "in_uv")
            ),
            self._ibo
        )

        overlay_shader = get_path("resources/shaders/overlay.glsl")

        self._overlay_program = self._context.program(
            vertex_shader=base_vertex_shader,
            fragment_shader=open(overlay_shader, "r", encoding="utf-8").read()
        )

        self._overlay_vao = self._context.vertex_array(
            self._overlay_program,
            (
                (self._vbo, "2f", "in_position"),
                (self._uvbo, "2f", "in_uv")
            ),
            self._ibo
        )

        self._main_fbo_target = self._context.texture(resolution, 4)
        self._main_fbo = self._context.framebuffer(color_attachments=(self._main_fbo_target,))

        self._texture = self._context.texture(resolution, 4)

        self._start_time = time()

        self.overlay_surf = pygame.Surface(resolution, flags=pygame.SRCALPHA)
        self.overlay_surf.fill((0, 0, 0, 0))
        self._overlay_tex = self._context.texture(resolution, 4)

    def __getitem__(self, key: str) -> Any:
        """ Get uniform value. """

        if self._suppress_uniform_errors and key not in self._program:
            return None

        return self._program[key].value
    
    def __setitem__(self, key: str, value: Any) -> None:
        """ Set uniform value. """

        if self._suppress_uniform_errors and key not in self._program:
            return

        self._program[key].value = value

    @property
    def exposure(self) -> float:
        """
        Exposure value.
        - EV = -1.0 -> 0.7x darker
        - EV = 0.0 -> Neutral
        - EV = 1.0 -> 1.4x brighter
        - EV = 2.0 -> 2.0x brighter (one full-stop)
        """
        return self["u_exposure"]
    
    @exposure.setter
    def exposure(self, value: float) -> None:
        self["u_exposure"] = value

    @property
    def hue(self) -> float:
        """
        Hue shift.
        - 0.0 -> Neutral
        - 0.5 -> 180 degree shift
        - 1.0 -> 360 degree shift (same as 0)
        """
        return self["u_hue"]
    
    @hue.setter
    def hue(self, value: float) -> None:
        self["u_hue"] = value

    @property
    def saturation(self) -> float:
        """
        Saturation multiplier.
        - 0.0 -> Grayscale
        - 1.0 -> Neutral
        - 2.0 -> 2x more saturated
        """
        return self["u_saturation"]
    
    @saturation.setter
    def saturation(self, value: float) -> None:
        self["u_saturation"] = value

    @property
    def value(self) -> float:
        """
        Value (blackness) multiplier.
        """
        return self["u_value"]
    
    @value.setter
    def value(self, value: float) -> None:
        self["u_value"] = value

    def reset(self) -> None:
        """ Reset all uniform states. """

        self["u_resolution"] = self._resolution

        self["u_exposure"] = 0.0
        self["u_hue"] = 0.0
        self["u_saturation"] = 1.0
        self["u_value"] = 1.0
        
        self.reset_shockwave_anim()

    def reset_shockwave_anim(self) -> None:
        """ Reset shockwave animation. """

        self["u_shockwave_pos"] = (0.0, 0.0)
        self["u_shockwave_start"] = -1.0

    def play_shockwave_anim(self, position: pygame.Vector2) -> None:
        """
        Start playing shockwave animation.
        
        Parameters
        ----------
        position
            Origin of the shockwave
        """

        self["u_shockwave_pos"] = (position.x, position.y)
        self["u_shockwave_start"] = time() - self._start_time

    def create_buffer_object(self,
            data: list[float] | list[int]
            ) -> moderngl.Buffer:
        """
        Create buffer object from array.
        
        Parameters
        ----------
        data
            A list of either floats or ints
        """

        dtype = "f" if isinstance(data[0], float) else "I"
        return self._context.buffer(array(dtype, data))
    
    def upload(self, surface: pygame.Surface) -> None:
        """ Upload surface data to texture. """

        # TODO: pygame.Surface.get_view is magnitudes faster than
        #       pygame.image.tobytes in my tests, but needs
        #       testing on other machines too.

        self._texture.write(surface.get_view("1"))

        self._overlay_tex.write(self.overlay_surf.get_view("1"))
        self.overlay_surf.fill((0, 0, 0, 0))

    def render(self) -> None:
        """ Render post-processing. """

        self["u_time"] = time() - self._start_time

        self._main_fbo.use()
        self._texture.use(0)
        self._vao.render()

        self._context.screen.use()
        self._overlay_tex.use(0)
        self._main_fbo_target.use(1)
        self._overlay_vao.render()