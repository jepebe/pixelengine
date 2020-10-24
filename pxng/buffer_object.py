import glm
from OpenGL.GL import (GL_ARRAY_BUFFER, glGenBuffers, glBindBuffer, glBufferData,
                       GL_DYNAMIC_DRAW, glEnableVertexAttribArray, GL_UNSIGNED_INT,
                       GL_UNSIGNED_SHORT, GL_UNSIGNED_BYTE, GL_FLOAT,
                       glVertexAttribPointer, GL_ELEMENT_ARRAY_BUFFER, GL_DOUBLE)


class BufferObject:
    def __init__(self, data_type, array_type=GL_ARRAY_BUFFER, max_size=10000):
        self._data_type = data_type
        self._array_type = array_type
        self._arr = glm.array(data_type()) * max_size
        self._index = 0
        self._vbo = glGenBuffers(1)
        self._changed = True

    @property
    def type(self):
        return self._data_type

    @property
    def dtype(self):
        return self._arr.dtype

    @property
    def index(self):
        return self._index

    def __len__(self):
        return self._index

    @property
    def changed(self):
        return self._changed

    @property
    def component_count(self):
        return len(self._data_type())

    @property
    def bytes_per_element(self):
        return self._arr.dt_size * self.component_count

    def set_value(self, value):
        self._arr[self._index] = value
        self._index += 1
        self._changed = True

    def reset(self):
        self._index = 0
        self._changed = True

    def bind(self, attrib_index):
        if self._index == 0:
            return False

        glBindBuffer(self._array_type, self._vbo)

        if self._changed:
            data = self._arr
            size = data.itemsize * self._index
            glBufferData(self._array_type, size, data.ptr, GL_DYNAMIC_DRAW)
            self._changed = False

            if self._array_type == GL_ARRAY_BUFFER:
                glEnableVertexAttribArray(attrib_index)
                count = self.component_count
                stride = self.bytes_per_element
                dtype = self.dtype

                if dtype == 'float32':
                    gl_type = GL_FLOAT
                elif dtype == 'float64':
                    gl_type = GL_DOUBLE
                elif dtype == 'uint8':
                    gl_type = GL_UNSIGNED_BYTE
                elif dtype == 'uint16':
                    gl_type = GL_UNSIGNED_SHORT
                elif dtype == 'uint32':
                    gl_type = GL_UNSIGNED_INT
                else:
                    raise UserWarning(f'Unknown data type: {dtype}')

                glVertexAttribPointer(attrib_index, count, gl_type, False, stride, None)

        return True
