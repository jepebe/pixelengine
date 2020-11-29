from typing import Tuple

import glm
import imageio
from numpy.core.multiarray import ndarray

import pxng
from pxng import resource
from OpenGL.GL import GL_TRIANGLES, GL_RGBA, GL_RGB, glGenTextures, \
    GL_TEXTURE_RECTANGLE, glBindTexture, glTexParameteri, GL_TEXTURE_MAG_FILTER, \
    GL_NEAREST, GL_TEXTURE_MIN_FILTER, glTexImage2D, GL_UNSIGNED_BYTE, glTexSubImage2D, \
    GL_BLEND, glDisable, GL_RED, glPixelStorei, GL_UNPACK_ALIGNMENT, glGetInteger


class SpriteRectangle:
    def __init__(self):
        program = pxng.ShaderProgram('SpriteShader')
        program.add_shader(resource('shaders/sprite.vert'), pxng.ShaderType.Vertex)
        program.add_shader(resource('shaders/sprite.frag'), pxng.ShaderType.Fragment)
        program.compile_and_link()

        program.add_uniform('projection_view', glm.mat4x4)
        program.add_uniform('model', glm.mat4x4)
        program.add_uniform('texture_matrix', glm.mat4x4)
        program.add_uniform('color', glm.vec4)
        program.add_uniform('sprite_texture', glm.ivec1)
        self._program = program

        self._vao = pxng.VertexArrayObject(GL_TRIANGLES)
        self._vao.attach_buffer(pxng.BufferObject(data_type=glm.vec3))  # vertex buffer
        self._vao.attach_buffer(pxng.BufferObject(data_type=glm.uvec2))  # texture buffer

        self._vao.add_quad(
            glm.vec3(0, 0, 0),
            glm.vec3(0, -1, 0),
            glm.vec3(1, -1, 0),
            glm.vec3(1, 0, 0),
        )

        self._vao.set_texture(
            glm.uvec2(0, 1),
            glm.uvec2(0, 0),
            glm.uvec2(1, 0),
            glm.uvec2(1, 1)
        )

    def draw(self, spaces: pxng.Spaces):
        if self._vao.bind():
            self._program.activate()
            self._program.set_uniform('projection_view', spaces.projection_view)
            self._program.set_uniform('model', spaces.model.m)
            self._program.set_uniform('texture_matrix', spaces.texture.m)
            self._program.set_uniform('color', spaces.tint)
            self._program.set_uniform('sprite_texture', 0)
            self._vao.draw()


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
            self._format = GL_RED

        self._rect = None

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def set_pixel(self, x, y, color: Tuple[int, int, int]):
        self._data[y, x] = color
        self._dirty = True

    def _set_unpack_alignment(self):
        self._unpack_alignment = glGetInteger(GL_UNPACK_ALIGNMENT)
        if self._width % 2 == 1 or self._width % 4 == 2:
            # Odd sized texture
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    def _reset_unpack_alignment(self):
        glPixelStorei(GL_UNPACK_ALIGNMENT, self._unpack_alignment)

    def _create(self):
        self._texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_RECTANGLE, self._texid)

        glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        d = self._data
        w = self._width
        h = self._height
        fmt = self._format

        self._set_unpack_alignment()
        glTexImage2D(GL_TEXTURE_RECTANGLE, 0, fmt, w, h, 0, fmt, GL_UNSIGNED_BYTE, d)
        self._reset_unpack_alignment()

        self._rect = SpriteRectangle()
        self._created = True

    def _update(self):
        glBindTexture(GL_TEXTURE_RECTANGLE, self._texid)

        d = self._data
        w = self._width
        h = self._height
        fmt = self._format

        self._set_unpack_alignment()
        glTexSubImage2D(GL_TEXTURE_RECTANGLE, 0, 0, 0, w, h, fmt, GL_UNSIGNED_BYTE, d)
        self._reset_unpack_alignment()

        self._updated = True

    def update(self):
        self._dirty = True

    def activate(self):
        if not self._created:
            self._create()

        if self._dirty:
            self._update()

        glBindTexture(GL_TEXTURE_RECTANGLE, self._texid)
        glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def deactivate(self):
        glBindTexture(GL_TEXTURE_RECTANGLE, 0)

    def _pre_draw(self, spaces: pxng.Spaces):
        self.activate()
        spaces.model.push()
        spaces.texture.push()

    def _post_draw(self, spaces: pxng.Spaces):
        self.deactivate()
        spaces.model.pop()
        spaces.texture.pop()

    def draw(self, spaces: pxng.Spaces):
        """
        Draw the sprite at the current position.

        Parameters
        ----------
        spaces : pxng.Spaces
            the current coordinate systems
        """
        self._pre_draw(spaces)
        spaces.model.translate((0, self._height, 0))  # anchor is upper left
        spaces.model.scale((self._width, self._height, 1))
        spaces.texture.scale(glm.vec3(self._width, self._height, 1))
        self._rect.draw(spaces)
        self._post_draw(spaces)

    def draw_partial(self, spaces: pxng.Spaces, x, y, width, height):
        """
        Draw a partial sprite using pixel coordinates for the partial image data.
        The coordinates represent a sub region in the sprite.

        Parameters
        ----------
        spaces: pxng.Spaces
            the current coordinate systems
        x: int
            x coordinate in pixel space
        y: int
            y coordinate in pixel space
        width: int
            width in number of pixels
        height: int
            height in number of pixels
        """
        self._pre_draw(spaces)
        spaces.model.translate((0, height, 0))  # anchor is upper left
        spaces.model.scale((width, height, 1))

        spaces.texture.translate(glm.vec3(x, y, 0))
        spaces.texture.scale(glm.vec3(width, height, 1))
        self._rect.draw(spaces)

        self._post_draw(spaces)

    @classmethod
    def create_from_image(cls, path):
        img_data = imageio.imread(path)
        return Sprite(img_data)
