import glfw
from OpenGL.GL import *

import pxng


def floatify(r, g, b):
    return r / 0xFF, g / 0xFF, b / 0xFF


black = floatify(0x00, 0x00, 0x00)
white = floatify(0xFF, 0xFF, 0xFF)
red = floatify(0x68, 0x37, 0x2B)
cyan = floatify(0x70, 0xA4, 0xB2)
violet = floatify(0x6F, 0x3D, 0x86)
green = floatify(0x58, 0x8D, 0x43)
blue = floatify(0x35, 0x28, 0x79)
yellow = floatify(0xB8, 0xC7, 0x6F)
orange = floatify(0x6F, 0x4F, 0x25)
brown = floatify(0x43, 0x39, 0x00)
light_red = floatify(0x9A, 0x67, 0x59)
dark_grey = floatify(0x44, 0x44, 0x44)
grey_2 = floatify(0x6C, 0x6C, 0x6C)
light_green = floatify(0x9A, 0xD2, 0x84)
light_blue = floatify(0x6C, 0x5E, 0xB5)
light_grey = floatify(0x95, 0x95, 0x95)


def update(window: pxng.Window):
    if window.is_key_pressed(glfw.KEY_SPACE):
        print(f'Space is pressed')

    if window.is_key_pressed(glfw.KEY_Q):
        window.close_window()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*light_blue, 1)

    glColor(*blue, 1)
    glTranslate(42, 42, 0)
    glBegin(GL_QUADS)
    glVertex(0, 200)
    glVertex(0, 0)
    glVertex(320, 0)
    glVertex(320, 200)
    glEnd()

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glColor(*light_blue, 1)
    glTranslatef(0, 18, 0)
    window.draw_string(0, 0, '    **** COMMODORE 64 BASIC V2 ****')
    glTranslatef(0, 18, 0)
    window.draw_string(0, 0, ' 64K RAM SYSTEM  38911 BASIC BYTES FREE')
    glTranslatef(0, 18, 0)
    window.draw_string(0, 0, 'READY.')


if __name__ == '__main__':
    window = pxng.Window(806, 568, 'C64', scale=2)
    window.frame = 0
    window.set_update_handler(update)
    window.start_event_loop()
