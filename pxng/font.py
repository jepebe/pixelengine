import freetype as ft
import numpy
from numpy.core.multiarray import ndarray


# This code is derived from the example in the *freetype-py* repository
# FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier


class Font:
    def __init__(self, filename, size):
        self._font_data: ndarray = None
        self._glyph_width = None
        self._glyph_height = None
        self._grid_width = 16
        self._grid_height = 6
        self._make_font(filename, size)

    @property
    def glyph_width(self):
        return self._glyph_width

    @property
    def glyph_height(self):
        return self._glyph_height

    @property
    def grid_width(self):
        return self._grid_width

    @property
    def grid_height(self):
        return self._grid_height

    @property
    def data(self) -> ndarray:
        return self._font_data

    def _make_font(self, filename, size):
        face = ft.Face(filename)
        face.set_char_size(size * 64)
        if not face.is_fixed_width:
            raise UserWarning('Font is not monotype')

        grid_height = self.grid_height
        grid_width = self.grid_width
        # Determine largest glyph size
        width, height, ascender, descender = 0, 0, 0, 0
        # start at 32 to skip 32 first ASCII characters
        for c in range(32, grid_width * grid_height + 32):
            face.load_char(chr(c), ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT)
            bitmap = face.glyph.bitmap
            width = max(width, bitmap.width)
            ascender = max(ascender, face.glyph.bitmap_top)
            descender = max(descender, bitmap.rows - face.glyph.bitmap_top)
        height = ascender + descender

        # Generate texture data
        z = numpy.zeros((height * grid_height, width * grid_width), dtype=numpy.ubyte)
        for j in range(grid_height):
            for i in range(grid_width):
                pos = chr(32 + j * grid_width + i)
                face.load_char(pos, ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT)
                bitmap = face.glyph.bitmap
                x = i * width + face.glyph.bitmap_left
                y = j * height + ascender - face.glyph.bitmap_top
                z[y:y + bitmap.rows, x:x + bitmap.width].flat = bitmap.buffer
        self._font_data = z
        self._glyph_width = width
        self._glyph_height = height
