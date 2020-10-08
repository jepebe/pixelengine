import glfw
from OpenGL.GL import *

from pxng.window import Window


def update(window):
    if window.is_key_pressed(glfw.KEY_SPACE):
        print(f'Space is pressed')

    if window.is_key_pressed(glfw.KEY_Q):
        window.close_window()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glClearColor(0.1, 0.1, 0.2, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()


if __name__ == "__main__":
    window = Window(640, 480, 'PixelEngine', scale=2)
    window.set_update_handler(update)
    window.start_event_loop()
