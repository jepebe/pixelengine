from math import copysign

import pxng
from pxng.colors import *
from pxng.keys import *


def update(window: pxng.Window):
    handle_input(window)

    window.draw_grid(tint=DARK_GREY)
    window.draw_text(10, 10, 'Text Rendering', tint=LIGHT_BLUE)

    # Use the bitmap font as something interesting to scroll through
    font: pxng.Font = window.context['font']
    font_data = font.data
    page_width = font.glyph_width * 2  # a character is 8 bytes and we can show 16 bytes
    page_height = font.glyph_height * font.grid_height
    page_count = font.grid_width // 2

    line = window.context['line']
    row_count = 0x20  # 32
    column_count = 0x10  # 16
    window.tint = LIGHT_GREEN
    for row in range(row_count):
        addr = line * column_count + row * column_count
        addr %= 0x10000
        row_txt = f'${addr:04X}'
        for col in range(column_count):
            # since we only show 16 columns we divide the bitmap into 8 pages
            page = ((row + line) // page_height) % page_count
            v = font_data[(row + line) % page_height, (col + page * page_width)]
            row_txt += f' {v & 0xFF:02X}'
        window.draw_text(15, 25 + row * 6, row_txt, scale=0.5)

    text = 'Text Rotated 90 degrees'
    window.draw_text(5, 215, text, scale=0.5, tint=LIGHT_ORANGE, angle=-90)

    window.tint = LIGHT_AZURE
    window.draw_text(230, 25, 'SPACE    : toggle auto', scale=0.5)
    window.draw_text(230, 31, 'UP       : 1 line up', scale=0.5)
    window.draw_text(230, 37, 'DOWN     : 1 line down', scale=0.5)
    window.draw_text(230, 43, 'PAGE UP  : 1 page up', scale=0.5)
    window.draw_text(230, 49, 'PAGE DOWN: 1 page down', scale=0.5)
    window.draw_text(230, 55, 'HOME     : go to top', scale=0.5)
    window.draw_text(230, 61, 'END      : go to end', scale=0.5)

    text = f'Frames rendered: {window.context["frame"]}'
    window.draw_text(10, 226, text, tint=LIGHT_YELLOW, scale=0.5)
    text = 'Auto scrolling' if not window.context['paused'] else 'Manual scrolling'
    window.draw_text(10, 232, text, tint=LIGHT_YELLOW, scale=0.5)

    if not window.context['paused']:
        window.context['frame'] += 1
        window.context['line'] += 1


def handle_input(window):
    if window.key_state(KEY_SPACE).pressed:
        window.context['paused'] = not window.context['paused']

    if window.key_state(KEY_Q).pressed:
        window.close_window()

    if window.key_state(KEY_UP).pressed:
        window.context['line'] -= 1

    if window.key_state(KEY_DOWN).pressed:
        window.context['line'] += 1

    if window.key_state(KEY_PAGE_UP).pressed:
        window.context['line'] -= 0x20

    if window.key_state(KEY_PAGE_DOWN).pressed:
        window.context['line'] += 0x20

    if window.key_state(KEY_HOME).pressed:
        window.context['line'] = 0x000

    if window.key_state(KEY_END).pressed:
        window.context['line'] = 0xFE0

    scroll = window.mouse.scroll_dy
    if window.mouse.hover and scroll != 0:
        window.context['line'] -= int(copysign(max(1.0, abs(scroll)), scroll))

    if window.context['line'] < 0:
        window.context['line'] = 0

    if window.context['line'] > 0xFE0:
        window.context['line'] = 0xFE0


if __name__ == "__main__":
    window = pxng.Window(640, 480, 'PixelEngine', scale=2)
    window.context['line'] = 0
    window.context['frame'] = 0
    window.context['paused'] = False
    window.context['font'] = window.create_default_font()

    window.set_update_handler(update)
    window.start_event_loop()
