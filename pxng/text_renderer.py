import glm

from OpenGL.GL import GL_ARRAY_BUFFER, glGenVertexArrays, glBindVertexArray, \
    glDrawArrays, GL_POINTS

import pxng


class FontRenderer:
    def __init__(self):
        self._vao = glGenVertexArrays(1)
        self._points = pxng.BufferObject(data_type=glm.vec3, array_type=GL_ARRAY_BUFFER)
        self._chars = pxng.BufferObject(data_type=glm.uvec1, array_type=GL_ARRAY_BUFFER)

        program = pxng.ShaderProgram('FontShader')
        program.add_shader(pxng.resource('shaders/font.vert'), pxng.ShaderType.Vertex)
        program.add_shader(pxng.resource('shaders/font.geom'), pxng.ShaderType.Geometry)
        program.add_shader(pxng.resource('shaders/font.frag'), pxng.ShaderType.Fragment)
        program.compile_and_link()

        program.add_uniform('projection_view', glm.mat4x4)
        program.add_uniform('model', glm.mat4x4)
        program.add_uniform('color', glm.vec4)
        program.add_uniform('size', glm.uvec1)
        program.add_uniform('sprite_texture', glm.ivec1)
        self._program = program

    def add_char(self, pos: glm.vec3, char: int):
        self._points.set_value(pos)
        self._chars.set_value(glm.uvec1(char))

    def reset(self):
        self._points.reset()
        self._chars.reset()

    def draw(self, spaces):
        glBindVertexArray(self._vao)
        if self._points.bind(0) and self._chars.bind(1):
            self._program.activate()
            self._program.set_uniform('projection_view', spaces.projection_view)
            self._program.set_uniform('model', spaces.model.m)
            self._program.set_uniform('color', spaces.tint)
            # self._program.set_uniform('size', 8)
            self._program.set_uniform('sprite_texture', 0)

            glDrawArrays(GL_POINTS, 0, len(self._points))

        glBindVertexArray(0)


class TextRenderer:
    def __init__(self, font: pxng.Font):
        self._font = font
        self._font_sprite = pxng.Sprite(self._font._font_data)
        self._renderer = FontRenderer()

    def draw_string(self, spaces: pxng.Spaces, x, y, text, scale=1.0, angle=0):
        self._renderer.reset()
        self._font_sprite.activate()

        angle = glm.radians(angle)

        dx = self._font.glyph_width
        for i, c in enumerate(text):
            self._renderer.add_char(glm.vec3(i * dx, 0, 0), ord(c))

        spaces.model.push()
        spaces.model.translate((x, y, 1))
        spaces.model.scale((scale, scale, 1))
        spaces.model.rotate(angle, (0, 0, 1))

        self._renderer.draw(spaces)

        spaces.model.pop()
        self._font_sprite.deactivate()
