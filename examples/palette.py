import colorsys

import glfw

import pxng
from pxng.colors import PALETTE, DARK_GREY, AZURE, LIGHT_GREEN


def update(window: pxng.Window):
    if window.is_key_pressed(glfw.KEY_SPACE):
        window.context['paused'] = not window.context['paused']

    if window.is_key_pressed(glfw.KEY_Q):
        window.close_window()

    window.draw_grid(size=5, tint=(0.125, 0.125, 0.125), factor=1)
    window.draw_grid(size=20, tint=DARK_GREY)

    window.draw_text(5, 5, "Palette", tint=LIGHT_GREEN)

    draw_named_palette(window, 10, 20)

    component = window.context['animated_component']
    draw_hsl(window, 10, 110, saturation=1.0)
    draw_hsl(window, 10, 170, saturation=component)

    draw_rgb(window, 200, 20, face='rg', component=component)
    draw_rgb(window, 200, 90, face='br', component=component)
    draw_rgb(window, 200, 160, face='gb', component=component)

    if not window.context['paused']:
        direction = window.context['animation_direction']
        window.context['animated_component'] += direction * 0.01
        ac = window.context['animated_component']
        if not 0 < ac < 1.0:
            window.context['animation_direction'] = -1 * direction
            window.context['animated_component'] = abs(ac)


def draw_named_palette(window, x, y):
    window.draw_text(x, y, "Named Colors", tint=AZURE, scale=0.5)
    y += 5
    size = 16
    for color_range in PALETTE:
        for index, color in enumerate(color_range):
            window.fill_rect(x, y + size * index, size, size, tint=color)
        x += size


def draw_rgb(window, x, y, face, component=0.0):
    # face can be any pair of (R, G, B)
    face = face.upper()
    u_axis = face[0]
    v_axis = face[1]
    c1 = ('R', 'G', 'B').index(u_axis)
    c2 = ('R', 'G', 'B').index(v_axis)

    if 'R' not in face:
        c3 = 0
        w_axis = 'R'
    elif 'G' not in face:
        c3 = 1
        w_axis = 'G'
    else:
        c3 = 2
        w_axis = 'B'

    title = f'RGB ({u_axis}{v_axis}) {w_axis}={component:0.02f}'
    window.draw_text(x, y, title, tint=AZURE, scale=0.5)
    y += 5
    size = 4
    steps = 15
    for u in range(steps):
        u = u / steps
        for i, v in enumerate(range(steps)):
            v = v / steps
            c = [0, 0, 0]
            c[c1] = u
            c[c2] = v
            c[c3] = component
            window.fill_rect(x + i * size, y, size, size, c)
        y += size


def draw_hsl(window, x, y, saturation):
    text = f'HSL Colors Saturation={saturation:.2f}'
    window.draw_text(10, y, text, tint=AZURE, scale=0.5)
    y += 5
    size = 5
    hue_steps = 35
    lightness_steps = 10
    for lightness in range(lightness_steps):
        for i, hue in enumerate(range(hue_steps)):
            h = hue / (hue_steps - 1)
            # extend range and start from 1 to avoid top white and bottom black row
            l = 1 - (lightness + 1) / (lightness_steps + 1)
            rgb = colorsys.hls_to_rgb(h, l, saturation)
            window.fill_rect(x + i * size, y, size, size, rgb)
        y += size


if __name__ == "__main__":
    window = pxng.Window(640, 480, 'PixelEngine', scale=2)
    window.context['paused'] = False
    window.context['animated_component'] = 0.0
    window.context['animation_direction'] = 1  # 1 or -1

    window.set_update_handler(update)
    window.start_event_loop()
