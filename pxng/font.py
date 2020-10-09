import freetype as ft
import numpy


# This code is derived from the example in the *freetype-py* repository
# FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
from numpy.core.multiarray import ndarray


class Font:
    def __init__(self, filename, size):
        self._font_data = self._make_font(filename, size)

    @staticmethod
    def _make_font(filename, size) -> ndarray:
        face = ft.Face(filename)
        face.set_char_size(size * 64)
        if not face.is_fixed_width:
            raise UserWarning('Font is not monotype')

        # Determine largest glyph size
        width, height, ascender, descender = 0, 0, 0, 0
        for c in range(32, 128):
            face.load_char(chr(c), ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT)
            bitmap = face.glyph.bitmap
            width = max(width, bitmap.width)
            ascender = max(ascender, face.glyph.bitmap_top)
            descender = max(descender, bitmap.rows - face.glyph.bitmap_top)
        height = ascender + descender

        # Generate texture data
        z = numpy.zeros((height * 6, width * 16), dtype=numpy.ubyte)
        for j in range(6):
            for i in range(16):
                pos = chr(32 + j * 16 + i)
                face.load_char(pos, ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT)
                bitmap = face.glyph.bitmap
                x = i * width + face.glyph.bitmap_left
                y = j * height + ascender - face.glyph.bitmap_top
                z[y:y + bitmap.rows, x:x + bitmap.width].flat = bitmap.buffer

        return z
