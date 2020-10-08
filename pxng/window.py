import time

import glfw


class Window:

    def __init__(self, width, height, title='', **kwargs):
        """
        Creates a new window.

        After the successful creation of a window the loop has
        to be manually started with *start_event_loop*.
        To draw, set the update handler with a *fn(window)* callback.

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

    def start_event_loop(self):
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
                glfw.set_window_title(self._window,
                                      f'{self.title} @ {self.fps:.0f} FPS')
                now = time.time()
                frame_count = 0

        glfw.terminate()

    def close_window(self):
        glfw.set_window_should_close(self._window, glfw.TRUE)

    def set_update_handler(self, handler):
        self._handler = handler
