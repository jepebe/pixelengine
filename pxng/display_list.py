from pxng.opengl import *


class DisplayList:
    def __init__(self, count=1):
        self._count = count
        self._created = False
        self._base = None
        self._next_list = 0
        self._create()

    def _create(self):
        self._base = glGenLists(self._count)
        self._created = True

    def start_display_list(self):
        #if not self._created:
        #    self._create()

        #if self._next_list >= self._count:
        #    raise UserWarning(f'max number of display lists reached: {self._count}')

        list_id = self._base + self._next_list
        glNewList(list_id, GL_COMPILE)
        self._next_list += 1
        return list_id

    def end_display_list(self):
        glEndList()

    def draw(self, indexes):
        glListBase(self._base)
        glCallLists(indexes)
