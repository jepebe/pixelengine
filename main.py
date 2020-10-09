import glfw
from OpenGL.GL import *

import pxng


def update(window):
    if window.is_key_pressed(glfw.KEY_SPACE):
        print(f'Space is pressed')

    if window.is_key_pressed(glfw.KEY_Q):
        window.close_window()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1)

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    # glEnable(GL_DEPTH_TEST)

    glColor(1, 0, 0.5, 1)
    sprite._x = 0
    sprite._y = 160
    glTranslate(0, 0, -0.1)
    sprite.draw()

    glColor(0, 1, 1, 1)
    sprite._x = 0
    sprite._y = 320
    sprite.draw()

    glColor(1, 1, 0, 1)
    sprite.x = 160
    sprite.y = 240
    sprite.draw()

    glColor(0, 1, 0, 1)
    glBegin(GL_QUADS)
    glVertex(0, window.height)
    glVertex(0, 0)
    glVertex(window.width, 0)
    glVertex(window.width, window.height)
    glVertex(0, 1)
    glVertex(0, 0)
    glVertex(1, 0)
    glVertex(1, 1)
    glEnd()


if __name__ == "__main__":
    font = pxng.Font('fonts/C64_Pro_Mono-STYLE.ttf', 20)
    sprite = pxng.Sprite(font._font_data, font._font_data.shape[1], font._font_data.shape[0])

    window = pxng.Window(640, 480, 'PixelEngine', scale=2)
    window.set_update_handler(update)
    window.start_event_loop()
