from OpenGL.GL import *
from numpy.core.multiarray import ndarray


class Sprite:
    def __init__(self, data: ndarray, width, height):
        self._data = data
        self._created = False
        self._texid = None
        self._x = 0
        self._y = 0
        self._width = width
        self._height = height

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    def _create(self):
        self._texid = glGenTextures(1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self._texid)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        d = self._data
        w = self._width
        h = self._height
        glTexImage2D(GL_TEXTURE_2D, 0, GL_ALPHA, w, h, 0, GL_ALPHA, GL_UNSIGNED_BYTE, d)

    def draw(self):
        if not self._created:
            self._create()
            self._created = True

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self._texid)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glPushMatrix()
        glTranslatef(self._x, self._y, 0)
        x = self._x
        y = self._y
        glBegin(GL_QUADS)
        glTexCoord2f(x, y), glVertex(0, -self._height)
        glTexCoord2f(x, y + 1), glVertex(0, 0)
        glTexCoord2f(x + 1, y + 1), glVertex(self._width, 0)
        glTexCoord2f(x + 1, y), glVertex(self._width, -self._height)
        glEnd()
        glPopMatrix()
