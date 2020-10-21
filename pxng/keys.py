from dataclasses import dataclass
from typing import Dict

import glfw

KEY_SPACE = glfw.KEY_SPACE
KEY_APOSTROPHE = glfw.KEY_APOSTROPHE
KEY_COMMA = glfw.KEY_COMMA
KEY_MINUS = glfw.KEY_MINUS
KEY_PERIOD = glfw.KEY_PERIOD
KEY_SLASH = glfw.KEY_SLASH
KEY_0 = glfw.KEY_0
KEY_1 = glfw.KEY_1
KEY_2 = glfw.KEY_2
KEY_3 = glfw.KEY_3
KEY_4 = glfw.KEY_4
KEY_5 = glfw.KEY_5
KEY_6 = glfw.KEY_6
KEY_7 = glfw.KEY_7
KEY_8 = glfw.KEY_8
KEY_9 = glfw.KEY_9
KEY_SEMICOLON = glfw.KEY_SEMICOLON
KEY_EQUAL = glfw.KEY_EQUAL
KEY_A = glfw.KEY_A
KEY_B = glfw.KEY_B
KEY_C = glfw.KEY_C
KEY_D = glfw.KEY_D
KEY_E = glfw.KEY_E
KEY_F = glfw.KEY_F
KEY_G = glfw.KEY_G
KEY_H = glfw.KEY_H
KEY_I = glfw.KEY_I
KEY_J = glfw.KEY_J
KEY_K = glfw.KEY_K
KEY_L = glfw.KEY_L
KEY_M = glfw.KEY_M
KEY_N = glfw.KEY_N
KEY_O = glfw.KEY_O
KEY_P = glfw.KEY_P
KEY_Q = glfw.KEY_Q
KEY_R = glfw.KEY_R
KEY_S = glfw.KEY_S
KEY_T = glfw.KEY_T
KEY_U = glfw.KEY_U
KEY_V = glfw.KEY_V
KEY_W = glfw.KEY_W
KEY_X = glfw.KEY_X
KEY_Y = glfw.KEY_Y
KEY_Z = glfw.KEY_Z
KEY_LEFT_BRACKET = glfw.KEY_LEFT_BRACKET
KEY_BACKSLASH = glfw.KEY_BACKSLASH
KEY_RIGHT_BRACKET = glfw.KEY_RIGHT_BRACKET
KEY_GRAVE_ACCENT = glfw.KEY_GRAVE_ACCENT
KEY_WORLD_1 = glfw.KEY_WORLD_1
KEY_WORLD_2 = glfw.KEY_WORLD_2
KEY_ESCAPE = glfw.KEY_ESCAPE
KEY_ENTER = glfw.KEY_ENTER
KEY_TAB = glfw.KEY_TAB
KEY_BACKSPACE = glfw.KEY_BACKSPACE
KEY_INSERT = glfw.KEY_INSERT
KEY_DELETE = glfw.KEY_DELETE
KEY_RIGHT = glfw.KEY_RIGHT
KEY_LEFT = glfw.KEY_LEFT
KEY_DOWN = glfw.KEY_DOWN
KEY_UP = glfw.KEY_UP
KEY_PAGE_UP = glfw.KEY_PAGE_UP
KEY_PAGE_DOWN = glfw.KEY_PAGE_DOWN
KEY_HOME = glfw.KEY_HOME
KEY_END = glfw.KEY_END
KEY_CAPS_LOCK = glfw.KEY_CAPS_LOCK
KEY_SCROLL_LOCK = glfw.KEY_SCROLL_LOCK
KEY_NUM_LOCK = glfw.KEY_NUM_LOCK
KEY_PRINT_SCREEN = glfw.KEY_PRINT_SCREEN
KEY_PAUSE = glfw.KEY_PAUSE
KEY_F1 = glfw.KEY_F1
KEY_F2 = glfw.KEY_F2
KEY_F3 = glfw.KEY_F3
KEY_F4 = glfw.KEY_F4
KEY_F5 = glfw.KEY_F5
KEY_F6 = glfw.KEY_F6
KEY_F7 = glfw.KEY_F7
KEY_F8 = glfw.KEY_F8
KEY_F9 = glfw.KEY_F9
KEY_F10 = glfw.KEY_F10
KEY_F11 = glfw.KEY_F11
KEY_F12 = glfw.KEY_F12
KEY_F13 = glfw.KEY_F13
KEY_F14 = glfw.KEY_F14
KEY_F15 = glfw.KEY_F15
KEY_F16 = glfw.KEY_F16
KEY_F17 = glfw.KEY_F17
KEY_F18 = glfw.KEY_F18
KEY_F19 = glfw.KEY_F19
KEY_F20 = glfw.KEY_F20
KEY_F21 = glfw.KEY_F21
KEY_F22 = glfw.KEY_F22
KEY_F23 = glfw.KEY_F23
KEY_F24 = glfw.KEY_F24
KEY_F25 = glfw.KEY_F25
KEY_KP_0 = glfw.KEY_KP_0
KEY_KP_1 = glfw.KEY_KP_1
KEY_KP_2 = glfw.KEY_KP_2
KEY_KP_3 = glfw.KEY_KP_3
KEY_KP_4 = glfw.KEY_KP_4
KEY_KP_5 = glfw.KEY_KP_5
KEY_KP_6 = glfw.KEY_KP_6
KEY_KP_7 = glfw.KEY_KP_7
KEY_KP_8 = glfw.KEY_KP_8
KEY_KP_9 = glfw.KEY_KP_9
KEY_KP_DECIMAL = glfw.KEY_KP_DECIMAL
KEY_KP_DIVIDE = glfw.KEY_KP_DIVIDE
KEY_KP_MULTIPLY = glfw.KEY_KP_MULTIPLY
KEY_KP_SUBTRACT = glfw.KEY_KP_SUBTRACT
KEY_KP_ADD = glfw.KEY_KP_ADD
KEY_KP_ENTER = glfw.KEY_KP_ENTER
KEY_KP_EQUAL = glfw.KEY_KP_EQUAL
KEY_LEFT_SHIFT = glfw.KEY_LEFT_SHIFT
KEY_LEFT_CONTROL = glfw.KEY_LEFT_CONTROL
KEY_LEFT_ALT = glfw.KEY_LEFT_ALT
KEY_LEFT_SUPER = glfw.KEY_LEFT_SUPER
KEY_RIGHT_SHIFT = glfw.KEY_RIGHT_SHIFT
KEY_RIGHT_CONTROL = glfw.KEY_RIGHT_CONTROL
KEY_RIGHT_ALT = glfw.KEY_RIGHT_ALT
KEY_RIGHT_SUPER = glfw.KEY_RIGHT_SUPER
KEY_MENU = glfw.KEY_MENU

_keys = [KEY_SPACE, KEY_APOSTROPHE, KEY_COMMA, KEY_MINUS, KEY_PERIOD,
         KEY_SLASH, KEY_0, KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8,
         KEY_9, KEY_SEMICOLON, KEY_EQUAL, KEY_A, KEY_B, KEY_C, KEY_D, KEY_E, KEY_F,
         KEY_G, KEY_H, KEY_I, KEY_J, KEY_K, KEY_L, KEY_M, KEY_N, KEY_O, KEY_P, KEY_Q,
         KEY_R, KEY_S, KEY_T, KEY_U, KEY_V, KEY_W, KEY_X, KEY_Y, KEY_Z,
         KEY_LEFT_BRACKET, KEY_BACKSLASH, KEY_RIGHT_BRACKET, KEY_GRAVE_ACCENT,
         KEY_WORLD_1, KEY_WORLD_2, KEY_ESCAPE, KEY_ENTER, KEY_TAB, KEY_BACKSPACE,
         KEY_INSERT, KEY_DELETE, KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP, KEY_PAGE_UP,
         KEY_PAGE_DOWN, KEY_HOME, KEY_END, KEY_CAPS_LOCK, KEY_SCROLL_LOCK, KEY_NUM_LOCK,
         KEY_PRINT_SCREEN, KEY_PAUSE, KEY_F1, KEY_F2, KEY_F3, KEY_F4, KEY_F5, KEY_F6,
         KEY_F7, KEY_F8, KEY_F9, KEY_F10, KEY_F11, KEY_F12, KEY_F13, KEY_F14, KEY_F15,
         KEY_F16, KEY_F17, KEY_F18, KEY_F19, KEY_F20, KEY_F21, KEY_F22, KEY_F23,
         KEY_F24, KEY_F25, KEY_KP_0, KEY_KP_1, KEY_KP_2, KEY_KP_3, KEY_KP_4, KEY_KP_5,
         KEY_KP_6, KEY_KP_7, KEY_KP_8, KEY_KP_9, KEY_KP_DECIMAL, KEY_KP_DIVIDE,
         KEY_KP_MULTIPLY, KEY_KP_SUBTRACT, KEY_KP_ADD, KEY_KP_ENTER, KEY_KP_EQUAL,
         KEY_LEFT_SHIFT, KEY_LEFT_CONTROL, KEY_LEFT_ALT, KEY_LEFT_SUPER,
         KEY_RIGHT_SHIFT, KEY_RIGHT_CONTROL, KEY_RIGHT_ALT, KEY_RIGHT_SUPER, KEY_MENU]


@dataclass
class KeyState:
    pressed: bool = False
    released: bool = False
    held: bool = False

    def __str__(self):
        return f'self.pressed={self.pressed} self.released={self.released} self.held={self.held}'


class KeyPoller:
    def __init__(self):
        self._key_states: Dict[int, KeyState] = {key: KeyState() for key in _keys}

    def poll_keys(self, window):
        for key, key_state in self._key_states.items():
            cur_state = glfw.get_key(window, key)
            pressed = cur_state == glfw.PRESS
            released = cur_state == glfw.RELEASE

            if pressed and not key_state.pressed and not key_state.held:
                key_state.pressed = True
                key_state.released = False
                key_state.held = True
            elif pressed and key_state.held:
                key_state.pressed = False
                key_state.released = False
                key_state.held = True
            elif released and key_state.held:
                key_state.pressed = False
                key_state.released = True
                key_state.held = False
            else:
                key_state.pressed = False
                key_state.released = False
                key_state.held = False

    def key_state(self, key) -> KeyState:
        return self._key_states[key]
