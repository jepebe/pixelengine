import pxng
from pxng.opengl import *


class TextRenderer:
    def __init__(self, font: pxng.Font, vertical_spacing=2):
        self._font = font
        self._vertical_spacing = vertical_spacing
        self._font_sprite = pxng.Sprite(self._font._font_data)
        self._display_list = pxng.DisplayList(8 * 16)
        self._initialized = False
        self._create_display_list()

    def _create_display_list(self):
        glPushMatrix()
        glLoadIdentity()
        sw = self._font.glyph_width
        sh = self._font.glyph_height
        for i in range(8 * 16):
            self._display_list.start_display_list()
            sx = i % 16
            sy = i // 16 - 2

            if i >= 32:
                glBegin(GL_QUADS)
                glTexCoord2i(sx * sw, sy * sh), glVertex(0, -sh)
                glTexCoord2i(sx * sw, sy * sh + sh), glVertex(0, 0)
                glTexCoord2i((sx + 1) * sw, sy * sh + sh), glVertex(sw, 0)
                glTexCoord2i((sx + 1) * sw, sy * sh), glVertex(sw, -sh)
                glEnd()

            glTranslatef(sw, 0, 0)
            self._display_list.end_display_list()
        glPopMatrix()
        self._initialized = True

    def draw_string(self, x, y, text, scale=1.0, angle=0):
        self._font_sprite.activate()

        glPushMatrix()
        sh = self._font.glyph_height
        glTranslatef(x, y, 0)
        glScalef(scale, scale, 1)
        glRotate(angle, 0, 0, 1)
        glTranslate(0, sh, 0)
        self._display_list.draw([ord(c) for c in text])
        glPopMatrix()
        self._font_sprite.deactivate()
