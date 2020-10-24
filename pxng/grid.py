import glm
from OpenGL.GL import GL_LINES

import pxng


class Grid:
    def __init__(self, width, height):
        program = pxng.ShaderProgram('GridShader')
        program.add_shader(pxng.resource('shaders/line.vert'), pxng.ShaderType.Vertex)
        program.add_shader(pxng.resource('shaders/line.frag'), pxng.ShaderType.Fragment)
        program.compile_and_link()

        program.add_uniform('projection_view', glm.mat4x4)
        program.add_uniform('model', glm.mat4x4)
        program.add_uniform('color', glm.vec4)
        program.add_uniform('resolution', glm.vec2)
        program.add_uniform('dash_size', glm.vec1)
        program.add_uniform('gap_size', glm.vec1)

        self._shader_program = program

        self._vao = pxng.VertexArrayObject(GL_LINES)
        self._vao.attach_buffer(pxng.BufferObject(data_type=glm.vec3))  # vertex buffer

        x = 1
        y = 1
        while x < width:
            self._vao.add_line(glm.vec3(x, 0, 0), glm.vec3(x, height, 0))
            x += 1

        while y < height:
            self._vao.add_line(glm.vec3(0, y, 0), glm.vec3(width, y, 0))
            y += 1

    def draw(self, spaces: pxng.Spaces, size, dash_size, gap_size):
        if self._vao.bind():
            spaces.model.push()
            spaces.model.scale((size, size, 1))
            program = self._shader_program
            program.activate()
            program.set_uniform('projection_view', spaces.projection_view)
            program.set_uniform('model', spaces.model.m)
            program.set_uniform('color', spaces.tint)
            program.set_uniform('resolution', glm.vec2(spaces.width, spaces.height))
            program.set_uniform('dash_size', dash_size)
            program.set_uniform('gap_size', gap_size)

            self._vao.draw()

            spaces.model.pop()
