import math
from collections import namedtuple

import glfw
import numpy as np

import pxng
from pxng.opengl import *


Range2D = namedtuple('Range2D', ['x1', 'y1', 'x2', 'y2'])


def update(window: pxng.Window):
    if window.is_key_pressed(glfw.KEY_SPACE):
        print(f'Space is pressed')

    if window.is_key_pressed(glfw.KEY_Q):
        window.close_window()

    if window.is_key_pressed(glfw.KEY_Z):
        window.context['zoom'] *= 0.9
        zoom = window.context['zoom']
        sprite = window.context['sprite']
        render_fractal(sprite, window.width, window.height, zoom)

    if window.is_key_pressed(glfw.KEY_X):
        window.context['zoom'] *= 1.1
        zoom = window.context['zoom']
        sprite = window.context['sprite']
        render_fractal(sprite, window.width, window.height, zoom)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1)

    glPushMatrix()
    sprite = window.context['sprite']
    window.draw_sprite(0, 0, sprite, scale=1)
    count = window.context['count']

    window.context['count'] += 1

    glPopMatrix()

    window.draw_string(0, 0, 'Fractal Renderer')


def create_fractal(pix: Range2D, frac: Range2D, iterations=256):
    x_scale = (frac.x2 - frac.x1) / (pix.x2 - pix.x1)
    y_scale = (frac.y2 - frac.y1) / (pix.y2 - pix.y1)
    fractal = []
    for y in range(pix.y1, pix.y2):
        for x in range(pix.x1, pix.x2):
            c = complex(x * x_scale * frac.x1, y * y_scale + frac.y1)
            z = complex(0, 0)

            n = 0
            while abs(z) < 2 and n < iterations:
                z = (z * z) + c
                n += 1
            fractal.append(n)
    return fractal


def render_fractal(sprite, w, h, zoom=1.0):
    frac = Range2D(-1 * zoom, -1 * zoom, 1 * zoom, 1 * zoom)
    fractal = create_fractal(Range2D(0, 0, w, h), frac)
    for y in range(h):
        for x in range(w):
            i = fractal[y * w + x]
            n = float(i)
            a = 0.1
            # @Eriksonn referred to by OLC
            r = 0.5 * math.sin(a * n) + 0.5
            g = 0.5 * math.sin(a * n + 2.094) + 0.5
            b = 0.5 * math.sin(a * n + 4.188) + 0.5
            sprite.set_pixel(x, y, (r * 255, g * 255, b * 255))


if __name__ == "__main__":
    w = 512
    h = 512
    data = np.zeros((h, w, 3), dtype=np.uint8)
    sprite = pxng.Sprite(data)
    render_fractal(sprite, w, h)
    window = pxng.Window(w, h, 'PixelEngine', scale=1)
    window.context = {'data': data, 'sprite': sprite, 'count': 0, 'zoom': 1}
    window.set_update_handler(update)
    window.start_event_loop()
