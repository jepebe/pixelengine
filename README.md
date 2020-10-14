# PXNG

*PXNG* is a python library that provides a simplified API for working with pixels, drawing shapes, writing text and interacting with input devices. It is inspired by the *olcPixelGameEngine* by OneLoneCoder.

## What it can do:
- Create a window for drawing. The window supports rendering at a lower virtual resolution. 
- Render text. The built in font is C64 styled.
- Render filled shapes. Currently only rectangles. :)
- Render sprites. Sprites can be scaled and blend with the background. Created from NumPy arrays. It is also possible to use *imageio* to read files directly in to sprites. Any changes in the data buffer of the sprite can be updated in the live rendering.
- Animated sprites. Using a sprite sheet *pxng* supports animation.
- Poll the keyboard for events.


## How to Install
Installation of `pxng` is done simply by: `pip install pxng`. The examples are not part of the distribution. 


## Examples
In the examples folder there are three applications that show how the library is used to perform different tasks. These examples does not show the most efficient way of doing the task, however.

1. Palette - By abusing `fill_rect` the following screenshot was created. The live rendering animates the color of the lower **HSL** view and all  of the **RGB** views.
![Screenshot of palette.py](https://github.com/jepebe/pixelengine/blob/master/images/palette.png?raw=true)

2. Animated Sprites - Shows some of the possibilities of rendering sprite sheets. All of the visible sprites in the screenshot are animated by  sub indexing the sprite sheet in a 8x8 grid.
![Screenshot of animated_sprites.py](https://github.com/jepebe/pixelengine/blob/master/images/animated_sprites.png?raw=true)

3. Text Rendering - This example shows animated rendering of text. The green field of hexadecimal numbers scrolls by as fast as it can.
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