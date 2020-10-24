import time

import glfw
import glm
from OpenGL.GL import GL_TRUE, glGetString, GL_VERSION, glViewport, glClearColor, \
    glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glEnable, glBlendFunc, \
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA

import pxng
import pxng.keys
import pxng.mouse
from pxng.grid import Grid
from pxng.colors import WHITE
from pxng.quad import Quad


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

        # switch to newer OpenGL version...
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)  # mac only
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

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

        glfw.set_input_mode(self._window, glfw.STICKY_KEYS, glfw.TRUE)
        glfw.make_context_current(self._window)
        glfw.swap_interval(1 if vsync else 0)

        gl_version = glGetString(GL_VERSION).decode('utf-8')
        print(f'OpenGL Version string: {gl_version}')

        self._spaces = pxng.Spaces(self.width, self.height)
        self._spaces.projection.m = glm.ortho(0, width, height, 0, -1, 1)
        self._spaces.view.scale((self.x_scale, self.y_scale, 1))

        self._text_renderer = pxng.TextRenderer(self.create_default_font())
        self._elapsed_time = 0
        self._current_tint = WHITE
        self._key_poller = pxng.keys.KeyPoller()
        self._mouse_poller = pxng.mouse.Mouse(self._window)

        self._quad = Quad()
        self._grid = Grid(self.width, self.height)

    def create_default_font(self) -> pxng.Font:
        font_path = pxng.resource('fonts/C64_Pro_Mono-STYLE.ttf')
        return pxng.Font(font_path, 8)

    def start_event_loop(self):
        glViewport(0, 0, self.width, self.height)
        self._loop()

    def key_state(self, key) -> pxng.keys.KeyState:
        return self._key_poller.key_state(key)

    @property
    def mouse(self) -> pxng.mouse.Mouse:
        """
        Returns the mouse state.

        Returns
        -------
        pxng.mouse.Mouse
        """
        return self._mouse_poller

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
            self._key_poller.poll_keys(self._window)
            self._mouse_poller._poll_mouse(self._window)

            self._spaces.push()
            self._spaces.tint = WHITE

            glClearColor(*self._color)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            now = time.time()
            self._elapsed_time = (now - elapsed_now)
            elapsed_now = now

            # draw call
            if self._handler is not None:
                self._handler(self)

            # render last batch of rects (if any)
            self._quad.draw_batch_if_started(self._spaces)

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

    def draw_sprite(self, x, y, sprite, scale=1.0, tint=None):
        self._quad.draw_batch_if_started(self._spaces)
        self._spaces.tint = tint
        self._spaces.model.push()
        self._spaces.model.translate((x, y, 0))
        self._spaces.model.scale((scale, scale, 1))
        sprite.draw(self._spaces)
        self._spaces.model.pop()

    def draw_text(self, x, y, text, scale=1.0, tint=None, angle=0):
        self._quad.draw_batch_if_started(self._spaces)
        self._spaces.tint = tint
        self._text_renderer.draw_string(self._spaces, x, y, text, scale, angle)

    def draw_partial_sprite(self, x, y, sprite, sx, sy, sw, sh, scale=1.0, tint=None):
        self._quad.draw_batch_if_started(self._spaces)
        self._spaces.tint = tint
        self._spaces.model.push()
        self._spaces.model.translate((x, y, 0))
        self._spaces.model.scale((scale, scale, 1))
        sprite.draw_partial(self._spaces, sx, sy, sw, sh)
        self._spaces.model.pop()

    def draw_grid(self, size=10, tint=None, dash_size=4, gap_size=4):
        self._quad.draw_batch_if_started(self._spaces)
        self._spaces.tint = tint
        self._grid.draw(self._spaces, size, dash_size, gap_size)

    def fill_rect(self, x, y, w, h, tint=None):
        self._quad.check_started()
        self._spaces.tint = tint
        self._quad.draw(self._spaces, x, y, w, h)

    @property
    def tint(self):
        return self._spaces.default_tint

    @tint.setter
    def tint(self, tint):
        self._spaces.default_tint = tint
