# PXNG

*PXNG* is a python library that provides a simplified API for working with pixels, drawing shapes, writing text and interacting with input devices. It is inspired by the *olcPixelGameEngine* by OneLoneCoder.

## What it can do:
- Create a window for drawing. The window supports rendering at a lower virtual resolution. 
- Render text. The built in font is C64 styled.
- Render filled shapes. Currently only rectangles. :)
- Render sprites. Sprites can be scaled and blend with the background. Created from NumPy arrays. It is also possible to use *imageio* to read files directly in to sprites. Any changes in the data buffer of the sprite can be updated in the live rendering.
- Animated sprites. Using a sprite sheet *pxng* supports animation.
- Poll the keyboard for events.


## How to install
Installation of `pxng` is done simply by: `pip install pxng`. The examples are not part of the distribution. 


## Getting started

Before venturing into the examples, let us try a __Hello, world!__ example first.

```python
import pxng
from pxng.colors import *
``` 

This will import the `pxng` library and get some named colors that we can use. 

```python
if __name__ == '__main__':
    window = pxng.Window(640, 480, 'PixelEngine', scale=2, vsync=True)
    window.set_update_handler(update)
    window.start_event_loop()
```

This will create a 640x480 window with a scale of 2. This scaling factor results in a _virtual_ resolution of 320x240. We set `vsync=true` to limit the frame rate to 60 frames per second (Hz). Finally we set the update handler to point to a function we have not made yet, called `update`.

```python
def update(window: pxng.Window):
    window.draw_text(100, 100, "Hello, world!", tint=LIGHT_GREEN)
```

The `update` function has a single argument that is provided by the framework and it is `window`. This is the context that you will use to draw and handle interaction. In this case we use the `draw_text` function to write our "Hello, world!" message at `(x, y) = (100, 100)` in a light green color. 

Running this should result in the following screenshot:

![Screenshot of text_rendering.py](https://github.com/jepebe/pixelengine/blob/master/images/hello_world.png?raw=true)
 

## Examples
In the examples folder there are three applications that show how the library is used to perform different tasks. These examples does not show the most efficient way of doing the task, however.

1. Palette - By abusing `fill_rect` the following screenshot was created. The live rendering animates the color of the lower **HSL** view and all  of the **RGB** views.

![Screenshot of palette.py](https://github.com/jepebe/pixelengine/blob/master/images/palette.png?raw=true)

2. Animated Sprites - Shows some of the possibilities of rendering sprite sheets. All of the visible sprites in the screenshot are animated by  sub indexing the sprite sheet in a 8x8 grid. Left click and drag to move one of the sprites (the largest running character) around.

![Screenshot of animated_sprites.py](https://github.com/jepebe/pixelengine/blob/master/images/animated_sprites.png?raw=true)

3. Text Rendering - This example shows animated rendering of text. The green field of hexadecimal numbers scrolls by as fast as it can. Press __space__ to stop the animation. Use the __up__ and __down__ arrow keys, __page up__ and __page down__ or __home__ and __end__ to navigate in the scrolling text. Mouse scrolling is also supported.

![Screenshot of text_rendering.py](https://github.com/jepebe/pixelengine/blob/master/images/text_rendering.png?raw=true)



## Copyrights

- C64 font - The font is included as part of the repository and the license
  is available here: https://style64.org/c64-truetype/license
- olcPixelGameEngine - https://github.com/OneLoneCoder/olcPixelGameEngine
- Freetype - The code for generating bitmap fonts as numpy arrays and rendering text with OpenGL Display Lists is copyrighted by Nicolas P. Rougier. 
  https://github.com/rougier/freetype-py/blob/master/examples/opengl.py
  
## Credits

- thekingphoenix and Bonsaiheldin for the character sprite
- para for particle effects