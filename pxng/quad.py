import glm
from OpenGL.GL import GL_TRIANGLES

import pxng
from pxng import resource


class Quad:
    def __init__(self):
        program = pxng.ShaderProgram('QuadShader')
        program.add_shader(resource('shaders/quad.vert'), pxng.ShaderType.Vertex)
        program.add_shader(resource('shaders/quad.frag'), pxng.ShaderType.Fragment)
        program.compile_and_link()

        program.add_uniform('projection_view', glm.mat4x4)

        self._shader_program = program

        self._vao = pxng.VertexArrayObject(GL_TRIANGLES)
        self._vao.attach_buffer(pxng.BufferObject(data_type=glm.vec3))  # vertex buffer
        self._vao.attach_buffer(pxng.BufferObject(data_type=glm.vec4))  # color buffer

        self._started = False

    def start_batch(self):
        self._vao.reset()
        self._started = True

    def check_started(self):
        if not self._started:
            self.start_batch()

    def draw(self, spaces: pxng.Spaces, x, y, w, h):
        p1 = glm.vec3(x, y, 0)
        p2 = glm.vec3(x, y + h, 0)
        p3 = glm.vec3(x + w, y + h, 0)
        p4 = glm.vec3(x + w, y, 0)

        self._vao.add_quad(p1, p2, p3, p4)
        tint = spaces.tint
        self._vao.set_colors(tint, tint, tint, tint)

    def draw_batch(self, spaces: pxng.Spaces):
        if self._vao.bind():
            program = self._shader_program
            program.activate()
            program.set_uniform('projection_view', spaces.projection_view)
            self._vao.draw()
            self._started = False

    def draw_batch_if_started(self, spaces):
        if self._started:
            self.draw_batch(spaces)
