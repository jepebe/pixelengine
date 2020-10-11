#!/usr/bin/env python3
# encoding: utf-8

from distutils.core import setup, Extension

fractal_module = Extension(
    'fractal._fractal',
    sources=['fractal/_fractal.c'],
)

setup(name='_fractal',
      version='0.1.0',
      description='Fractal calculator',
      ext_modules=[fractal_module])
