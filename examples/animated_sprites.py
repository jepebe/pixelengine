import pxng
from pxng.colors import LIGHT_GREEN, DARK_GREY
from pxng.keys import KEY_SPACE, KEY_Q


def update(window: pxng.Window):
    if window.key_state(KEY_SPACE).pressed:
        window.context['paused'] = not window.context['paused']

    if window.key_state(KEY_Q).pressed:
        window.close_window()

    paused = window.context['paused']

    window.draw_grid(size=5, tint=(0.125, 0.125, 0.125), factor=1)
    window.draw_grid(size=20, tint=DARK_GREY)

    window.draw_text(5, 5, "Animated Sprites", tint=LIGHT_GREEN)

    flame_sprite = window.context['flame_sprite']
    if not paused:
        flame_sprite.advance_time(window.elapsed_time)
    window.draw_sprite(250, 10, flame_sprite, 0.5)

    fire_sprite = window.context['fire_sprite']
    if not paused:
        fire_sprite.advance_time(window.elapsed_time)
    window.draw_sprite(200, 240 - 128, fire_sprite, 1)
    window.draw_sprite(30, 240 - 64, fire_sprite, 0.5)

    fire2_sprite = window.context['fire2_sprite']
    if not paused:
        fire2_sprite.advance_time(window.elapsed_time)
    window.draw_sprite(105, 240 - 128, fire2_sprite, 1)

    pale_blue = window.context['pale_blue']
    if not paused:
        pale_blue.advance_time_all(window.elapsed_time)
    pale_blue.set_current_animation('walk_left')
    window.draw_sprite(70, 40, pale_blue, scale=0.5)
    window.draw_sprite(90, 40, pale_blue, scale=1)
    window.draw_sprite(120, 40, pale_blue, scale=2)
    window.draw_sprite(170, 40, pale_blue, scale=3)

    pale_blue.set_current_animation('run_right')
    window.draw_sprite(0-40, 40, pale_blue, scale=4)

    pale_blue.set_current_animation('shoot_right')
    window.draw_sprite(120, 200, pale_blue)

    pale_blue.set_current_animation('shoot_left')
    window.draw_sprite(170, 200, pale_blue)

    pale_blue.set_current_animation('idle_right')
    window.draw_sprite(0, 200, pale_blue)

    pale_blue.set_current_animation('idle_left')
    window.draw_sprite(70, 200, pale_blue)

    if not window.context['paused']:
        window.context['frame'] += 1


if __name__ == "__main__":
    spr = pxng.Sprite.create_from_image('sprites/pale_blue_original.png')
    pale_blue = pxng.AnimatedSprite(spr, grid_size=(8, 8))
    pale_blue.set_animation('idle_left', [(x, 0) for x in range(5)], fps=5)
    pale_blue.set_animation('idle_right', [(x, 1) for x in range(5)], fps=5)
    pale_blue.set_animation('walk_left', [(x, 2) for x in range(8)], fps=10)
    pale_blue.set_animation('run_left', [(x, 2) for x in range(8)], fps=20)
    pale_blue.set_animation('walk_right', [(x, 3) for x in range(8)], fps=10)
    pale_blue.set_animation('run_right', [(x, 3) for x in range(8)], fps=20)
    pale_blue.set_animation('shoot_left', [(x, 4) for x in range(5)], fps=10)
    pale_blue.set_animation('shoot_right', [(x, 5) for x in range(5)], fps=10)

    spr = pxng.Sprite.create_from_image('sprites/lighter_flame_01.png')
    flame_sprite = pxng.AnimatedSprite(spr, grid_size=(8, 8))

    spr = pxng.Sprite.create_from_image('sprites/fire_01.png')
    fire_sprite = pxng.AnimatedSprite(spr, grid_size=(8, 8))
    spr = pxng.Sprite.create_from_image('sprites/fire_02.png')
    fire2_sprite = pxng.AnimatedSprite(spr, grid_size=(8, 8))

    window = pxng.Window(640, 480, 'PixelEngine', scale=2)

    window.context['frame'] = 0
    window.context['paused'] = False
    window.context['flame_sprite'] = flame_sprite
    window.context['fire_sprite'] = fire_sprite
    window.context['fire2_sprite'] = fire2_sprite
    window.context['pale_blue'] = pale_blue

    window.set_update_handler(update)
    window.start_event_loop()
