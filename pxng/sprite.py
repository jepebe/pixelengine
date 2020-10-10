from typing import Tuple

from numpy.core.multiarray import ndarray
from pxng.opengl import *


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
        glEnable(GL_TEXTURE_RECTANGLE)
        glBindTexture(GL_TEXTURE_RECTANGLE, self._texid)

        glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        d = self._data
        w = self._width
        h = self._height
        fmt = self._format
        glTexImage2D(GL_TEXTURE_RECTANGLE, 0, fmt, w, h, 0, fmt, GL_UNSIGNED_BYTE, d)
        self._created = True

    def _update(self):
        glEnable(GL_TEXTURE_RECTANGLE)
        glBindTexture(GL_TEXTURE_RECTANGLE, self._texid)

        d = self._data
        w = self._width
        h = self._height
        fmt = self._format
        glTexSubImage2D(GL_TEXTURE_RECTANGLE, 0, 0, 0, w, h, fmt, GL_UNSIGNED_BYTE, d)
        self._updated = True

    def update(self):
        self._dirty = True

    def activate(self):
        if not self._created:
            self._create()

        if self._dirty:
            self._update()

        glEnable(GL_TEXTURE_RECTANGLE)
        glBindTexture(GL_TEXTURE_RECTANGLE, self._texid)
        glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        if self._format in (GL_ALPHA, GL_RGBA):
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def deactivate(self):
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_RECTANGLE)

    def _pre_draw(self):
        self.activate()
        glPushMatrix()

    def _post_draw(self):
        self.deactivate()
        glPopMatrix()

    def draw(self):
        self._pre_draw()
        glTranslate(0, self._height, 0)

        glBegin(GL_QUADS)
        glTexCoord2i(0, 0), glVertex(0, -self._height)
        glTexCoord2i(0, self._height), glVertex(0, 0)
        glTexCoord2i(self._width, self._height), glVertex(self._width, 0)
        glTexCoord2i(self._width, 0), glVertex(self._width, -self._height)
        glEnd()

        self._post_draw()

    def draw_partial(self, x, y, width, height):
        """
        Draw a partial sprite using pixel coordinates for the partial image data.

        Parameters
        ----------
        x: int
        y: int
        width: int
        height: int
        """
        self._pre_draw()
        glTranslate(0, height, 0)  # anchor is upper left

        glBegin(GL_QUADS)
        glTexCoord2i(x, y), glVertex(0, -height)
        glTexCoord2i(x, y + height), glVertex(0, 0)
        glTexCoord2i(x + width, y + height), glVertex(width, 0)
        glTexCoord2i(x + width, y), glVertex(width, -height)
        glEnd()

        self._post_draw()
