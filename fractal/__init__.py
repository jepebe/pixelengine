from collections import namedtuple as _namedtuple

Range2D = _namedtuple('Range2D', ['x1', 'y1', 'x2', 'y2'])
import numpy
print(numpy.get_include())
from .py_fractal import py_create_fractal
from ._fractal import create_fractal
