from copy import copy

import glm


class CoordinateSystem:

    def __init__(self):
        self._m = glm.mat4x4(1)
        self._stack = []

    def translate(self, vec3):
        self._m = glm.translate(self._m, vec3)

    def scale(self, vec3):
        self._m = glm.scale(self._m, vec3)

    def rotate(self, angle, vec3):
        self._m = glm.rotate(self._m, angle, vec3)

    def push(self):
        self._stack.insert(0, copy(self._m))

    def load_identity(self):
        self._m = glm.mat4x4(1)

    def pop(self):
        self._m = self._stack.pop(0)

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, m: glm.mat4x4):
        self._m = m


class Spaces:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._projection = CoordinateSystem()
        self._view = CoordinateSystem()
        self._model = CoordinateSystem()
        self._texture = CoordinateSystem()
        self._default_tint = glm.vec4(1)
        self._tint = self._default_tint

    @property
    def projection(self) -> CoordinateSystem:
        return self._projection

    @property
    def view(self) -> CoordinateSystem:
        return self._view

    @property
    def model(self) -> CoordinateSystem:
        return self._model

    @property
    def texture(self) -> CoordinateSystem:
        return self._texture

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def projection_view(self) -> glm.mat4x4:
        return self.projection.m * self.view.m

    @property
    def tint(self) -> glm.vec4:
        return self._tint

    @tint.setter
    def tint(self, tint: glm.vec4):
        if tint is None:
            tint = self.default_tint

        if len(tint) == 3:
            tint = glm.vec4(*tint, 1)
        else:
            tint = glm.vec4(*tint)
        self._tint = tint

    @property
    def default_tint(self):
        return self._default_tint

    @default_tint.setter
    def default_tint(self, tint):
        self._default_tint = tint

    def push(self):
        self.projection.push()
        self.view.push()
        self.model.push()
        self.texture.push()

    def pop(self):
        self.projection.pop()
        self.view.pop()
        self.model.pop()
        self.texture.pop()
