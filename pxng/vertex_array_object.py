from typing import List

import glm
import pxng

import OpenGL.GL as gl


class VertexArrayObject:
    def __init__(self, primitive):
        self._primitive = primitive
        self._buffers: List[pxng.BufferObject] = []
        self._indices = pxng.BufferObject(data_type=self.index_data_type,
                                          array_type=gl.GL_ELEMENT_ARRAY_BUFFER)
        self._vao = gl.glGenVertexArrays(1)

    def attach_buffer(self, vbo: pxng.BufferObject):
        self._buffers.append(vbo)
        return len(self._buffers) - 1

    def add_quad(self, p1, p2, p3, p4):
        i = self._buffers[0].index
        self._buffers[0].set_value(p1)
        self._buffers[0].set_value(p2)
        self._buffers[0].set_value(p3)
        self._buffers[0].set_value(p4)
        self._indices.set_value(glm.u16vec3(i, i + 1, i + 3))
        self._indices.set_value(glm.u16vec3(i + 1, i + 2, i + 3))

    def add_triangle(self, p1, p2, p3):
        i = self._buffers[0].index
        self._buffers[0].set_value(p1)
        self._buffers[0].set_value(p2)
        self._buffers[0].set_value(p3)
        self._indices.set_value(glm.u16vec3(i, i + 1, i + 2))

    def add_line(self, p1, p2):
        i = self._buffers[0].index
        self._buffers[0].set_value(p1)
        self._buffers[0].set_value(p2)
        self._indices.set_value(glm.u16vec2(i, i + 1))

    def add_point(self, p1):
        i = self._buffers[0].index
        self._buffers[0].set_value(p1)
        self._indices.set_value(glm.u16vec1(i))

    def set_colors(self, *args: glm.vec4, target=1):
        for c in args:
            self._buffers[target].set_value(c)

    def set_texture(self, *args: glm.vec2 or glm.uvec2, target=1):
        for c in args:
            self._buffers[target].set_value(c)

    def create(self):
        gl.glBindVertexArray(self._vao)

        for index, vbo in enumerate(self._buffers):
            vbo.bind(index)

        self._indices.bind(None)

    def reset(self):
        self._indices.reset()
        for vbo in self._buffers:
            vbo.reset()

    def draw(self):
        index_count = len(self._indices) * self.primitive_component_count
        gl.glDrawElements(self._primitive, index_count, gl.GL_UNSIGNED_SHORT, None)

    @property
    def index_data_type(self):
        if self._primitive == gl.GL_TRIANGLES:
            return glm.u16vec3
        elif self._primitive == gl.GL_LINES:
            return glm.u16vec2
        elif self._primitive == gl.GL_POINTS:
            return glm.u16vec1
        else:
            raise UserWarning(f'Unknown primitive type {self._primitive}')

    @property
    def primitive_component_count(self):
        if self._primitive == gl.GL_TRIANGLES:
            return 3
        elif self._primitive == gl.GL_LINES:
            return 2
        elif self._primitive == gl.GL_POINTS:
            return 1
        else:
            raise UserWarning(f'Unknown primitive type {self._primitive}')

    def bind(self):
        gl.glBindVertexArray(self._vao)
        if self._indices.bind(None):
            if any(vbo.changed for vbo in self._buffers):
                self.create()
            return True
        gl.glBindVertexArray(0)
        return False
