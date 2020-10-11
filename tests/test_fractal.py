from fractal import Range2D
import fractal


def test_range2d():
    a = Range2D(1, 2, 3, 4)
    b = Range2D(0.1, 0.2, 0.3, 0.4)
    fractal.calculate_fractal(a, b, 100)
