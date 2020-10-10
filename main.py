import glfw
import imageio

import pxng
from pxng.opengl import *


def update(window: pxng.Window):
    if window.is_key_pressed(glfw.KEY_SPACE):
        print(f'Space is pressed')

    if window.is_key_pressed(glfw.KEY_Q):
        window.close_window()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.4, 1)

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    # glEnable(GL_DEPTH_TEST)

    glColor(1, 1, 0, 1)
    value = 0x00
    for row in range(0x10):
        addr = 0xC000 + row * 0x10
        row_txt = f'${addr:04X}'
        for col in range(0x00, 0x10):
            row_txt += f' {value & 0xFF:02X}'
            value += 1
        window.draw_string(0, row * 10, row_txt, scale=0.5)

    for row in range(8):
        row_txt = f'{row:02X}:'
        for col in range(0x00, 0x10):
            row_txt += f' {chr(row * 16 + col)}'
        window.draw_string(0, 200 + row * 10, row_txt, scale=0.5)

    window.draw_sprite(250, 150, window._text_renderer._font_sprite, 0.5)

    glColor(1, 1, 1, 1)
    anim_frame = window.context['anim_frame']
    x = anim_frame % 10
    y = anim_frame // 10
    y = 5
    w = 96
    h = 103
    window.draw_partial_sprite(220, 0, sprite, x * w, y + y * h, w, h)
    window.context['anim_frame'] += 1 if window.context['frame'] % 10 == 0 else 0
    #window.context['anim_frame'] += 1
    if window.context['anim_frame'] == 10:
        window.context['anim_frame'] = 0

    window.context['frame'] += 1


if __name__ == "__main__":
    img = imageio.imread('sprites/link.png')
    sprite = pxng.Sprite(img)
    window = pxng.Window(640, 480, 'PixelEngine', scale=2)
    window.context['anim_frame'] = 0
    window.context['frame'] = 0
    window.context['sprite'] = sprite

    window.set_update_handler(update)
    window.start_event_loop()
