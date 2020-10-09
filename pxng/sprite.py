from typing import Tuple

from OpenGL.GL import *
from numpy.core.multiarray import ndarray


class Sprite:
    def __init__(self, data: ndarray):
        self._data = data
        self._created = False
        self._dirty = False
        self._texid = None
        self._width = data.shape[1]
        self._height = data.shape[0]
        self._components = 1
        if len(data.shape) > 2:
            self._components = data.shape[2]

        if self._components == 4:
            self._format = GL_RGBA
        elif self._components == 3:
            self._format = GL_RGB
        elif self._components == 1:
            self._format = GL_ALPHA

    def set_pixel(self, x, y, color: Tuple[int, int, int]):
        self._data[y, x] = color
        self._dirty = True

    def _create(self):
        self._texid = glGenTextures(1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self._texid)

        d = self._data
        w = self._width
        h = self._height
        fmt = self._format
        glTexImage2D(GL_TEXTURE_2D, 0, fmt, w, h, 0, fmt, GL_UNSIGNED_BYTE, d)
        self._created = True

    def _update(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self._texid)

        d = self._data
        w = self._width
        h = self._height
        fmt = self._format
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, w, h, fmt, GL_UNSIGNED_BYTE, d)
        self._updated = True

    def update(self):
        self._dirty = True

    def _pre_draw(self):
        if not self._created:
            self._create()

        if self._dirty:
            self._update()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self._texid)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        if self._format in (GL_ALPHA, GL_RGBA):
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glPushMatrix()

    def _post_draw(self):
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()

    def draw(self):
        self._pre_draw()
        glTranslate(0, self._height, 0)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0), glVertex(0, -self._height)
        glTexCoord2f(0, 1), glVertex(0, 0)
        glTexCoord2f(1, 1), glVertex(self._width, 0)
        glTexCoord2f(1, 0), glVertex(self._width, -self._height)
        glEnd()

        self._post_draw()

    def draw_partial(self, x, y, width, height, scale=1):
        self._pre_draw()

        dx = 1 / self._width
        dy = 1 / self._height
        glTranslate(0, height, 0)

        glBegin(GL_QUADS)
        glTexCoord2f(x * dx, y * dy), glVertex(0, -height)
        glTexCoord2f(x * dx, y * dy + height * dy), glVertex(0, 0)
        glTexCoord2f(x * dx + width * dx, y * dy + height * dy), glVertex(width, 0)
        glTexCoord2f(x * dx + width * dx, y * dy), glVertex(width, -height)
        glEnd()

        self._post_draw()
