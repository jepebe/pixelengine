# This module is a convenience import to bring the gl namespace into another module
# usage: from pxng.opengl import *
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
from OpenGL.GL import glTexEnvf, GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE
from OpenGL.GL import glClear, glClearColor, glColor
from OpenGL.GL import glLoadIdentity, glOrtho, glPushMatrix
from OpenGL.GL import glMatrixMode, GL_PROJECTION, GL_MODELVIEW, glPopMatrix
from OpenGL.GL import glViewport
from OpenGL.GL import glScalef, glTranslatef, glScale, glTranslate, glRotate, glRotatef
from OpenGL.GL import glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from OpenGL.GL import GL_RGBA, GL_RGB, GL_ALPHA
from OpenGL.GL import GL_UNSIGNED_BYTE
from OpenGL.GL import GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER
from OpenGL.GL import GL_TEXTURE_RECTANGLE
from OpenGL.GL import GL_NEAREST, GL_LINEAR
from OpenGL.GL import glEnable, glDisable
from OpenGL.GL import glGenTextures, glBindTexture, glTexImage2D
from OpenGL.GL import glTexSubImage2D, glTexParameterf, glTexParameteri
from OpenGL.GL import glBegin, glEnd, GL_QUADS, GL_LINES, GL_LINE, GL_LINE_STIPPLE
from OpenGL.GL import glLineStipple
from OpenGL.GL import glTexCoord2f, glTexCoord2i, glVertex
from OpenGL.GL import GL_COMPILE
from OpenGL.GL import glGenLists, glNewList, glEndList, glCallLists, glListBase
