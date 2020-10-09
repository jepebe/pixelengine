import os
import time
from pathlib import Path

import glfw
from OpenGL.GL import glLoadIdentity, glScalef, glTranslatef, glOrtho, glPushMatrix
from OpenGL.GL import glMatrixMode, GL_PROJECTION, GL_MODELVIEW, glPopMatrix, glViewport

import pxng


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
                Turn off or on vsync, default is false.
            resizable: bool
                Indicate if the windows should be resizable.
            x_scale: float
                Scaling in 'x' direction.
            y_scale: float
                Scaling in 'y' direction.
            scale: float
                Sets 'x_scale' and 'y_scale' to the same value.
        """
        if not glfw.init():
            raise UserWarning('Unable to initialize glfw')
        self.fps = 0
        self._handler = None
        self._title = title
        self.width = width
        self.height = height

        resizable = False
        if 'resizable' in kwargs:
            resizable = glfw.TRUE if kwargs['resizable'] else glfw.FALSE
        glfw.window_hint(glfw.RESIZABLE, resizable)

        vsync = False
        if 'vsync' in kwargs:
            vsync = bool(kwargs['vsync'])

        self.x_scale = kwargs['x_scale'] if 'x_scale' in kwargs else 1
        self.y_scale = kwargs['y_scale'] if 'y_scale' in kwargs else 1
        if 'scale' in kwargs:
            self.x_scale = self.y_scale = kwargs['scale']

        self._window = glfw.create_window(width, height, title, None, None)

        if not self._window:
            glfw.terminate()
            raise UserWarning('Unable to create window')

        glfw.make_context_current(self._window)
        glfw.swap_interval(1 if vsync else 0)

        font_path = Path(__file__).parent / 'resources/fonts/C64_Pro_Mono-STYLE.ttf'
        self._font = pxng.Font(str(font_path), 8)
        w = self._font._font_data.shape
        self._font_sprite = pxng.Sprite(self._font._font_data)

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

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        glfw.set_window_title(self._window, self._title)

    def _loop(self):
        frame_count = 0
        now = time.time()
        while not glfw.window_should_close(self._window):
            glLoadIdentity()
            glScalef(self.x_scale, self.y_scale, 1)
            # draw call
            if self._handler is not None:
                self._handler(self)

            # Swap front and back buffers
            glfw.swap_buffers(self._window)

            # Poll for and process events
            glfw.poll_events()
            frame_count += 1
            elapsed_time = (time.time() - now)
            self.fps = frame_count / elapsed_time

            if elapsed_time >= 1:
                title = f'{self.title} @ {self.fps:.0f} FPS'
                glfw.set_window_title(self._window, title)
                now = time.time()
                frame_count = 0

        glfw.terminate()

    def close_window(self):
        glfw.set_window_should_close(self._window, glfw.TRUE)

    def set_update_handler(self, handler):
        self._handler = handler

    def draw_sprite(self, x, y, sprite, scale=1):
        glPushMatrix()
        glTranslatef(x, y, 0)
        glScalef(scale, scale, 1)
        sprite.draw()
        glPopMatrix()

    def draw_string(self, x, y, text):
        glPushMatrix()
        sw = self._font.glyph_width
        sh = self._font.glyph_height
        glTranslatef(x, y, 0)
        for c in text:
            i = ord(c)
            sx = i % 16
            sy = i // 16 - 2
            self._font_sprite.draw_partial(sx * sw, sy * sh, sw, sh)
            glTranslatef(sw, 0, 0)
        glPopMatrix()

    def draw_partial_sprite(self, x, y, sprite, sx, sy, sw, sh):
        glPushMatrix()
        glTranslatef(x, y, 0)
        sprite.draw_partial(sx, sy, sw, sh)
        glPopMatrix()
