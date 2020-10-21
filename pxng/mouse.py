from dataclasses import dataclass
from typing import Tuple

import glfw

MOUSE_BUTTON_1 = glfw.MOUSE_BUTTON_1
MOUSE_BUTTON_2 = glfw.MOUSE_BUTTON_2
MOUSE_BUTTON_3 = glfw.MOUSE_BUTTON_3
MOUSE_BUTTON_4 = glfw.MOUSE_BUTTON_4
MOUSE_BUTTON_5 = glfw.MOUSE_BUTTON_5
MOUSE_BUTTON_6 = glfw.MOUSE_BUTTON_6
MOUSE_BUTTON_7 = glfw.MOUSE_BUTTON_7
MOUSE_BUTTON_8 = glfw.MOUSE_BUTTON_8
MOUSE_BUTTON_LEFT = glfw.MOUSE_BUTTON_LEFT
MOUSE_BUTTON_RIGHT = glfw.MOUSE_BUTTON_RIGHT
MOUSE_BUTTON_MIDDLE = glfw.MOUSE_BUTTON_MIDDLE


@dataclass
class MouseButtonState:
    pressed: bool = False
    """
    bool: This is true if the mouse button was pressed
    """

    released: bool = False
    """
    bool: This is true when the mouse button is released.
    """

    held: bool = False
    """
    bool: This is true from the moment of pressed until released.
    """

    def __str__(self):
        return f'self.pressed={self.pressed} self.released={self.released} self.held={self.held}'


class Mouse:
    def __init__(self, glfw_window):
        self._buttons = {
            MOUSE_BUTTON_1: MouseButtonState(),
            MOUSE_BUTTON_2: MouseButtonState(),
            MOUSE_BUTTON_3: MouseButtonState(),
            MOUSE_BUTTON_4: MouseButtonState(),
            MOUSE_BUTTON_5: MouseButtonState(),
            MOUSE_BUTTON_6: MouseButtonState(),
            MOUSE_BUTTON_7: MouseButtonState(),
            MOUSE_BUTTON_8: MouseButtonState(),
        }

        self._x = 0
        self._y = 0
        self._dx = 0
        self._dy = 0
        self._hover = False
        self._scroll_dx = 0
        self._scroll_dy = 0

        glfw.set_input_mode(glfw_window, glfw.STICKY_MOUSE_BUTTONS, glfw.TRUE)
        glfw.set_scroll_callback(glfw_window, self._scroll_callback)

    @property
    def hover(self) -> bool:
        """
        Is the mouse cursor hovering over the window?
        Returns
        -------
        bool
        """
        return self._hover

    @property
    def pos(self) -> Tuple[float, float]:
        """
        Returns the current mouse position as a tuple of floats
        Returns
        -------
        tuple of (float, float)
        """
        return self._x, self._y

    @property
    def x(self) -> float:
        """
        Returns the mouse x position
        Returns
        -------
        float
        """
        return self._x

    @property
    def y(self) -> float:
        """
        Returns the mouse y position
        Returns
        -------
        float
        """
        return self._y

    @property
    def dx(self) -> float:
        """
        Returns the mouse delta position in x direction since the last poll
        Returns
        -------
        float
        """
        return self._dx

    @property
    def dy(self) -> float:
        """
        Returns the mouse delta position in y direction since the last poll
        Returns
        -------
        float
        """
        return self._dy

    @property
    def scroll_dx(self) -> float:
        """
        Returns the currently accumulated amount of scrolling in the x direction.
        Beware that the scroll accumulator is reset after this call.
        Returns
        -------
        float
        """
        dx = self._scroll_dx
        return dx

    @property
    def scroll_dy(self) -> float:
        """
        Returns the currently accumulated amount of scrolling in the y direction.
        Beware that the scroll accumulator is reset after this call.
        Returns
        -------
        float
        """
        dy = self._scroll_dy
        self._scroll_dy = 0
        return dy

    @property
    def scroll(self) -> Tuple[float, float]:
        """
        Returns the currently accumulated amount of scrolling in the both directions.
        Beware that the scroll accumulator is reset after this call.
        Returns
        -------
        float
        """
        return self.scroll_dx, self._scroll_dy

    @property
    def button_left(self) -> MouseButtonState:
        """
        Returns the state for the left mouse button.
        Returns
        -------
        MouseButtonState
        """
        return self._buttons[MOUSE_BUTTON_LEFT]

    @property
    def button_right(self) -> MouseButtonState:
        """
        Returns the state for the right mouse button.
        Returns
        -------
        MouseButtonState
        """
        return self._buttons[MOUSE_BUTTON_RIGHT]

    @property
    def button_middle(self) -> MouseButtonState:
        """
        Returns the state for the middle mouse button.
        Returns
        -------
        MouseButtonState
        """
        return self._buttons[MOUSE_BUTTON_MIDDLE]

    def button_state(self, button_id) -> MouseButtonState:
        """
        Returns the state for any mouse button.
        Parameters
        ----------
        button_id: One of MOUSE_BUTTON_n where n={1, .. , 8, LEFT, RIGHT, MIDDLE}
        Returns
        -------
        MouseButtonState
        """
        return self._buttons[button_id]

    def _poll_mouse(self, window):
        hover_state = glfw.get_window_attrib(window, glfw.HOVERED)
        self._hover = True if hover_state == 1 else False

        if self._hover:
            x, y = glfw.get_cursor_pos(window)
            self._dx = self._x - x
            self._dy = self._y - y
            self._x = x
            self._y = y

            for btn, btn_state in self._buttons.items():
                cur_state = glfw.get_mouse_button(window, btn)
                pressed = cur_state == glfw.PRESS
                released = cur_state == glfw.RELEASE

                if pressed and not btn_state.pressed and not btn_state.held:
                    btn_state.pressed = True
                    btn_state.released = False
                    btn_state.held = True
                elif pressed and btn_state.held:
                    btn_state.pressed = False
                    btn_state.released = False
                    btn_state.held = True
                elif released and btn_state.held:
                    btn_state.pressed = False
                    btn_state.released = True
                    btn_state.held = False
                else:
                    btn_state.pressed = False
                    btn_state.released = False
                    btn_state.held = False

    def _scroll_callback(self, window, x, y):
        self._scroll_dx += x
        self._scroll_dy += y
