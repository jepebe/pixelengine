import glfw
import imageio
from OpenGL.GL import *

import pxng


def update(window: pxng.Window):
    if window.is_key_pressed(glfw.KEY_SPACE):
        print(f'Space is pressed')

    if window.is_key_pressed(glfw.KEY_Q):
        window.close_window()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1)

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    # glEnable(GL_DEPTH_TEST)

    glColor(1, 1, 0, 1)
    window.draw_string(160, 160, 'Hello, world!')

    x = window.frame % 8
    y = window.frame // 8
    window.draw_partial_sprite(150, 150, sprite, x * 150, y * 150, 150, 150)
    window.frame += 1 if window.frame % 50 == 0 else 0
    if window.frame == 32:
        window.frame = 0


    # glColor(0, 1, 0, 1)
    # glBegin(GL_QUADS)
    # glVertex(0, window.height)
    # glVertex(0, 0)
    # glVertex(window.width, 0)
    # glVertex(window.width, window.height)
    # glVertex(0, 1)
    # glVertex(0, 0)
    # glVertex(1, 0)
    # glVertex(1, 1)
    # glEnd()


if __name__ == "__main__":
    img = imageio.imread('sprites/explosion.png')
    sprite = pxng.Sprite(img)
    window = pxng.Window(640, 480, 'PixelEngine', scale=2)
    window.frame = 0
    window.set_update_handler(update)
    window.start_event_loop()
