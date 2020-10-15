import glfw

import pxng
from pxng.colors import DARK_GREY, LIGHT_YELLOW, LIGHT_GREEN, LIGHT_BLUE, LIGHT_ORANGE


def update(window: pxng.Window):
    if window.is_key_pressed(glfw.KEY_SPACE):
        window.context['paused'] = not window.context['paused']

    if window.is_key_pressed(glfw.KEY_Q):
        window.close_window()

    window.draw_grid(tint=DARK_GREY)
    window.draw_text(10, 10, 'Text Rendering', tint=LIGHT_BLUE)

    frame = window.context['frame']
    row_count = 0x20  # 32
    column_count = 0x10  # 16
    start_row = 0x00 + frame % (0xFFF - row_count - 1)
    window.set_tint(LIGHT_GREEN)
    for row in range(row_count):
        addr = start_row * column_count + row * column_count
        row_txt = f'${addr:04X}'
        for col in range(column_count):
            row_txt += f' {(addr + col) >> 2 & 0xFF:02X}'
        window.draw_text(15, 25 + row * 6, row_txt, scale=0.5)

    text = 'Text Rotated 90 degrees'
    window.draw_text(240, 25, text, scale=0.5, tint=LIGHT_ORANGE, angle=90)

    text = f'Frames rendered: {frame}'
    window.draw_text(10, 230, text, tint=LIGHT_YELLOW, scale=0.5)

    if not window.context['paused']:
        window.context['frame'] += 1


if __name__ == "__main__":
    window = pxng.Window(640, 480, 'PixelEngine', scale=2)
    window.context['frame'] = 0
    window.context['paused'] = False

    window.set_update_handler(update)
    window.start_event_loop()
