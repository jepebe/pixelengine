from enum import Enum
import os.path
from typing import List

import glm
import OpenGL.GL as gl


class ShaderType(Enum):
    Vertex = gl.GL_VERTEX_SHADER
    Fragment = gl.GL_FRAGMENT_SHADER
    Geometry = gl.GL_GEOMETRY_SHADER


class _Shader:
    def __init__(self, path, shader_type: ShaderType):
        self._path = path
        self._shader_type = shader_type
        self._id = None
        self._timestamp = os.path.getmtime(path)
        self._failed_version = None
        self._attached = False

    @property
    def id(self):
        return self._id

    @property
    def last_modified(self):
        return self._timestamp

    @property
    def path(self):
        return self._path

    @property
    def type(self):
        return self._shader_type

    @property
    def has_changed(self):
        return self.last_modified != os.path.getmtime(self.path)

    @property
    def needs_compile(self):
        return self._id is None or self.has_changed

    def compile(self):
        with open(self.path, 'r') as fh:
            source = fh.read()
            self._timestamp = os.path.getmtime(self.path)

        if self._failed_version == self._timestamp:
            return

        if self._id is None:
            self._id = gl.glCreateShader(self._shader_type.value)

        gl.glShaderSource(self._id, source)
        gl.glCompileShader(self._id)

        status = gl.glGetShaderiv(self._id, gl.GL_COMPILE_STATUS, None)
        if status == gl.GL_FALSE:
            log = gl.glGetShaderInfoLog(self._id)

            print(f'An error occurred during compilation of: {self._path}')
            print('-' * 20)
            print(f'{log.decode("utf-8")}')
            print('-' * 20)
            self._failed_version = self._timestamp
        else:
            self._failed_version = None

        return status == gl.GL_TRUE

    def failed_compile(self):
        return self._failed_version is not None

    @property
    def attached(self):
        return self._attached

    @attached.setter
    def attached(self, attached):
        self._attached = attached

    def __repr__(self):
        status = self.failed_compile()
        return f'{self._path} id: {self._id} @ {self._timestamp} - status: {status}'


class ShaderProgram:
    def __init__(self, name, frag_data_location=0, frag_data_name='out_color'):
        self._name = name
        self._shaders: List[_Shader] = []
        self._id = None
        self._frag_data_loc = frag_data_location
        self._frag_data_name = frag_data_name
        self._uniforms = {}

    def add_shader(self, path, shader_type: ShaderType):
        self._shaders.append(_Shader(path, shader_type))

    def add_uniform(self, name, data_type):
        self._uniforms[name] = {
            'loc': self.get_uniform_location(name),
            'type': data_type,
            'fn': self._get_gl_function_for_type(data_type)
        }

    @staticmethod
    def _get_gl_function_for_type(data_type):
        if data_type == glm.mat4x4:
            def fn(loc, value):
                gl.glUniformMatrix4fv(loc, 1, False, glm.value_ptr(value))
            return fn
        elif data_type == glm.dvec4:
            def fn(loc, value):
                gl.glUniform4dv(loc, 1, glm.value_ptr(value))
            return fn
        elif data_type == glm.vec4:
            def fn(loc, value):
                gl.glUniform4fv(loc, 1, glm.value_ptr(value))
            return fn
        elif data_type == glm.vec3:
            def fn(loc, value):
                gl.glUniform3fv(loc, 1, glm.value_ptr(value))
            return fn
        elif data_type == glm.vec2:
            def fn(loc, value):
                gl.glUniform2fv(loc, 1, glm.value_ptr(value))
            return fn
        elif data_type == glm.vec1:
            return gl.glUniform1f
        elif data_type == glm.ivec1:
            return gl.glUniform1i
        elif data_type == glm.uvec1:
            return gl.glUniform1ui
        elif data_type == glm.bvec1:
            return gl.glUniform1ui
        else:
            raise UserWarning(f'Unknown data type: {data_type}')

    def _create(self):
        if self._id is None:
            self._id = gl.glCreateProgram()

        for shader in self._shaders:
            if shader.needs_compile:
                shader.compile()

            if shader.failed_compile():
                # One of the shaders did not compile correctly -> skip linking step
                return False

        return self._link_shader()

    def needs_recompile(self):
        for shader in self._shaders:
            if shader.needs_compile:
                return True
        return False

    def activate(self):
        gl.glUseProgram(self._id)

    def _link_shader(self):
        for shader in self._shaders:
            if shader.attached:
                gl.glDetachShader(self._id, shader.id)
            gl.glAttachShader(self._id, shader.id)
            shader.attached = True

        gl.glBindFragDataLocation(self._id, self._frag_data_loc, self._frag_data_name)

        gl.glLinkProgram(self._id)
        status = gl.glGetProgramiv(self._id, gl.GL_LINK_STATUS, None)
        if status == gl.GL_FALSE:
            log = gl.glGetProgramInfoLog(self._id)
            print(f'An error occurred during linking of: {self._name}')
            print('-' * 20)
            print(f'{log.decode("utf-8")}')
            print('-' * 20)
            return False
        return True

    def get_uniform_location(self, name):
        return gl.glGetUniformLocation(self._id, name)

    def set_uniform(self, name, value):
        u = self._uniforms[name]
        u['fn'](u['loc'], value)

    def compile_and_link(self) -> bool:
        return self._create()
