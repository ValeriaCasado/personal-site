import numpy as np
from collections.abc import Callable

def countIterationsUntilDivergent(c, threshold):
    z = complex(0, 0)
    for iteration in range(threshold):
        z = (z*z) + c

        if abs(z) > 4:
            break
        pass
    return iteration


DEFAULT_REAL_RANGE = (-2.25, 0.75)
DEFAULT_IMAGINARY_RANGE = (-1.5, 1.5)

def get_new_range(real_range: tuple, imaginary_range: tuple, coord: tuple, density) -> tuple[tuple[int]]:
    """
    Given a coordinate in a 2D space, 
    Where the x values are within a range :real_range: and y values :imaginary_range:
    Return a new real and imaginary range < current range, based around a coordinate

    :real_range: x axis range (i.e default (-2.25, 0.75))
    :imaginary_range: y axis range (i.e default (-1.5, 1.5))
    :coord: the coordinate in the 1000x1000 system: I.e 50, 56
    :density: Number of values in x and y
    """

    if real_range == None:
        return DEFAULT_REAL_RANGE, DEFAULT_IMAGINARY_RANGE

    print(real_range, imaginary_range)
    real = np.linspace(real_range[0], real_range[1], density)
    imaginary = np.linspace(imaginary_range[0], imaginary_range[1], density)

    unit_x = real[1]-real[0]
    unit_y = imaginary[1]-imaginary[0]

    print(coord)
    coord_x, coord_y = coord
    val_x, val_y = real[coord_x], imaginary[coord_y]

    new_x_range = (val_x-unit_x*100, val_x+unit_x*100)
    new_y_range = (val_y-unit_y*100, val_y+unit_y*100)
    return new_x_range, new_y_range



def mandlebrot(
    real_range: tuple[float] = (-2.25, 0.75), 
    imaginary_range: tuple[float] = (-1.5, 1.5),
    threshold: int = 100, 
    density: int = 1000,
    emit_function: Callable=lambda *args: None):

    if real_range is None and imaginary_range is None: 
        real_range = (-2.25, 0.75)
        imaginary_range = (-1.5, 1.5)

    x0, x1 = real_range
    y0, y1 = imaginary_range

    realAxis = np.linspace(x0, x1, density)
    imaginaryAxis = np.linspace(y0, y1, density)

    # 2-D array to represent mandelbrot atlas
    atlas = np.empty((density, density))

    # color each point in the atlas depending on the iteration count
    for j, iy in enumerate(imaginaryAxis):
        for i, ix in enumerate(realAxis):
            c = complex(ix, iy)
            atlas[j, i] = countIterationsUntilDivergent(c, threshold)

        emit_function({
            'row_idx': j,
            'values': atlas[j].tolist()
        })
    
    return atlas
