import time
from pathlib import Path

import glfw
import pxng
from pxng.colors import WHITE
from pxng.opengl import *


class Window:

    def __init__(self, width, height, title='', **kwargs):
        """
        Creates a new window.

        After the successful creation of a window the loop has
        to be manually started with *start_event_loop*.
        To draw, use *set_update_handler* with a *fn(window)* callback.

        Parameters
        ----------
        width: int
            Width of window.
        height: int
            Height of window.
        title: str
            Title to show in title bar.
        **kwargs
            vsync: bool
                Turn off or on vsync. default=False
            resizable: bool
                Indicate if the windows should be resizable. default=False
            x_scale: float
                Scaling in 'x' direction. default=1
            y_scale: float
                Scaling in 'y' direction. default=1
            scale: float
                Sets 'x_scale' and 'y_scale' to the same value.
            hdpi: bool
                Use HDPI if available. Default=False
            color: tuple of float
                Set the background color. RGB or RGBA supported
        """
        if not glfw.init():
            raise UserWarning('Unable to initialize glfw')
        self.fps = 0
        self._handler = None
        self._title = title
        self.width = width
        self.height = height
        self.context = {}

        resizable = glfw.FALSE
        if 'resizable' in kwargs:
            resizable = glfw.TRUE if kwargs['resizable'] else glfw.FALSE
        glfw.window_hint(glfw.RESIZABLE, resizable)

        hdpi = glfw.FALSE
        if 'hdpi' in kwargs:
            hdpi = glfw.TRUE if kwargs['hdpi'] else glfw.FALSE
        glfw.window_hint(glfw.COCOA_RETINA_FRAMEBUFFER, hdpi)

        vsync = False
        if 'vsync' in kwargs:
            vsync = bool(kwargs['vsync'])

        self.x_scale = kwargs['x_scale'] if 'x_scale' in kwargs else 1
        self.y_scale = kwargs['y_scale'] if 'y_scale' in kwargs else 1
        if 'scale' in kwargs:
            self.x_scale = self.y_scale = kwargs['scale']

        self._window = glfw.create_window(width, height, title, None, None)

        self._color = (0, 0, 0, 1)
        if 'color' in kwargs:
            self._color = kwargs['color']

        if not self._window:
            glfw.terminate()
            raise UserWarning('Unable to create window')

        glfw.make_context_current(self._window)
        glfw.swap_interval(1 if vsync else 0)
        glfw.set_input_mode(self._window, glfw.STICKY_KEYS, glfw.TRUE)

        font_path = Path(__file__).parent / 'resources/fonts/C64_Pro_Mono-STYLE.ttf'
        # font_path = Path(__file__).parent / 'resources/fonts/JetBrainsMono-Bold.ttf'
        self._text_renderer = pxng.TextRenderer(pxng.Font(str(font_path), 8))
        self._elapsed_time = 0
        self._current_tint = WHITE

    def start_event_loop(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_MODELVIEW)
        self._loop()

    def get_key(self, glfw_key):
        return glfw.get_key(self._window, glfw_key)

    def is_key_pressed(self, glfw_key):
        return self.get_key(glfw_key) == glfw.PRESS

    def is_key_released(self, glfw_key):
        return self.get_key(glfw_key) == glfw.RELEASE

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        glfw.set_window_title(self._window, self._title)

    @property
    def elapsed_time(self) -> float:
        return self._elapsed_time

    def _loop(self):
        frame_count = 0
        fps_now = time.time()
        elapsed_now = time.time()
        while not glfw.window_should_close(self._window):
            glLoadIdentity()
            glScalef(self.x_scale, self.y_scale, 1)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glClearColor(*self._color)

            now = time.time()
            self._elapsed_time = (now - elapsed_now)
            elapsed_now = now
            # draw call
            if self._handler is not None:
                self._handler(self)

            # Swap front and back buffers
            glfw.swap_buffers(self._window)

            # Poll for and process events
            glfw.poll_events()
            frame_count += 1
            fps_time_delta = (time.time() - fps_now)
            self.fps = frame_count / fps_time_delta

            if fps_time_delta >= 1:
                title = f'{self.title} @ {self.fps:.0f} FPS'
                glfw.set_window_title(self._window, title)
                fps_now = time.time()
                frame_count = 0

        glfw.terminate()

    def close_window(self):
        glfw.set_window_should_close(self._window, glfw.TRUE)

    def set_update_handler(self, handler):
        self._handler = handler

    @property
    def tint(self):
        return self._current_tint

    @tint.setter
    def tint(self, color):
        self._current_tint = color

    def draw_sprite(self, x, y, sprite, scale=1.0, tint=None):
        self._set_color(tint)
        glPushMatrix()
        glTranslatef(x, y, 0)
        glScalef(scale, scale, 1)
        sprite.draw()
        glPopMatrix()

    def draw_text(self, x, y, text, scale=1.0, tint=None, angle=0):
        self._set_color(tint)
        self._text_renderer.draw_string(x, y, text, scale, angle)

    def draw_partial_sprite(self, x, y, sprite, sx, sy, sw, sh, scale=1.0, tint=None):
        self._set_color(tint)
        glPushMatrix()
        glTranslatef(x, y, 0)
        glScalef(scale, scale, 1)
        sprite.draw_partial(sx, sy, sw, sh)
        glPopMatrix()

    def draw_grid(self, size=10, tint=None, factor=4, pattern=0xAAAA):
        self._set_color(tint)
        glLineStipple(factor, pattern)
        glEnable(GL_LINE_STIPPLE)
        x = size
        y = size
        glBegin(GL_LINES)
        while x < self.width:
            glVertex(x, 0)
            glVertex(x, self.height)
            x += size
        while y < self.height:
            glVertex(0, y)
            glVertex(self.width, y)
            y += size
        glEnd()

    def fill_rect(self, x, y, w, h, tint=None):
        glPushMatrix()
        self._set_color(tint)
        glTranslatef(x, y, 0)
        glBegin(GL_QUADS)
        glVertex(0, h)
        glVertex(0, 0)
        glVertex(w, 0)
        glVertex(w, h)
        glEnd()
        glPopMatrix()

    def _set_color(self, tint):
        if tint is None:
            tint = self._current_tint
        glColor(*tint)
