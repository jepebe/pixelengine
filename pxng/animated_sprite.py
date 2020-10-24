from typing import Tuple, List

import pxng


class AnimatedSprite:
    def __init__(self, sprite: pxng.Sprite, grid_size: Tuple[int, int]):
        self._sprite = sprite
        self._grid_width = grid_size[0]
        self._grid_height = grid_size[1]

        self._animations = {}
        all_frames = self._create_frames(self._grid_width, self._grid_height)
        self.set_animation('default', all_frames, 30)
        self.set_current_animation('default')

        self._sw = self._sprite.width // self._grid_width
        self._sh = self._sprite.height // self._grid_height

    def _create_frames(self, w, h):
        return [(i % w, i // w) for i in range(w * h)]

    def set_animation(self, name: str, frames: List[Tuple[int, int]], fps: int):
        self._animations[name] = {
            'name': name,
            'frames': frames,
            'fps': fps,
            'time_delta': 1 / fps,
            'accumulated_time': 0,
            'current_frame': 0,
            'frame_count': len(frames)
        }

    def set_current_animation(self, name):
        self._current_animation = self._animations[name]

    def advance_time_all(self, elapsed_time):
        for item in self._animations.values():
            item['accumulated_time'] += elapsed_time

            if item['accumulated_time'] >= item['time_delta']:
                item['accumulated_time'] = 0
                item['current_frame'] += 1

            if item['current_frame'] >= item['frame_count']:
                item['current_frame'] = 0

    def advance_time(self, elapsed_time):
        item = self._current_animation
        item['accumulated_time'] += elapsed_time

        if item['accumulated_time'] >= item['time_delta']:
            item['accumulated_time'] = 0
            item['current_frame'] += 1

        if item['current_frame'] >= item['frame_count']:
            item['current_frame'] = 0

    def draw(self, spaces: pxng.Spaces):
        animation = self._current_animation
        current_frame = animation['current_frame']
        x, y = animation['frames'][current_frame]

        w = self._sw
        h = self._sh

        self._sprite.draw_partial(spaces, x * w, y * h, w, h)


