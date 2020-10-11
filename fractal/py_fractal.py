from fractal import Range2D


def py_create_fractal(pix: Range2D, frac: Range2D, iterations=256):
    x_scale = (frac.x2 - frac.x1) / (pix.x2 - pix.x1)
    y_scale = (frac.y2 - frac.y1) / (pix.y2 - pix.y1)
    fractal = []
    for y in range(pix.y1, pix.y2):
        for x in range(pix.x1, pix.x2):
            c = complex(x * x_scale * frac.x1, y * y_scale + frac.y1)
            z = complex(0, 0)

            n = 0
            while abs(z) < 2 and n < iterations:
                z = (z * z) + c
                n += 1
            fractal.append(n)
    return fractal
