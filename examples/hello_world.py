import pxng
from pxng.colors import *


def update(window: pxng.Window):
    window.draw_text(100, 100, "Hello, world!", tint=LIGHT_GREEN)


if __name__ == '__main__':
    window = pxng.Window(640, 480, 'PixelEngine', scale=2, vsync=True)
    window.set_update_handler(update)
    window.start_event_loop()
