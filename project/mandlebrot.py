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
  width=100
  half_width=50
  div = density - 1
  coord_x, coord_y = coord
  if coord_x <= width or coord_y <= width or coord_x >= density - width or coord_y >= density - width:
    return real_range, imaginary_range

  else:
    
    real_unit = (abs(real_range[1])+abs(real_range[0]))/div
    im_unit = (abs(imaginary_range[1])+abs(imaginary_range[0]))/div

    x0, x1 = coord_x-half_width, coord_x+half_width
    y0, y1 = coord_y-half_width, coord_y+half_width

    x0, x1 = real_range[0] + x0*real_unit,real_range[0] + x1*real_unit
    y0, y1 = imaginary_range[0] + y0*im_unit, imaginary_range[0] + y1*im_unit

    return (x0, x1), (y0, y1)

def mandelbrot(
    real_range: tuple[float] = (-2.25, 0.75), 
    imaginary_range: tuple[float] = (-1.5, 1.5),
    threshold: int = 120, 
    density: int = 1000,
    coordinate_in_range: tuple[int] = None,
    emit_function: Callable = lambda *args:None):

    if coordinate_in_range:
        x, y = coordinate_in_range
        real_range, imaginary_range = get_new_range(
        real_numbers=realAxis,
        imaginary_numbers=imaginaryAxis,
        coord_x=x,
        coord_y=y,
        density=density
    ) 

    x0, x1 = real_range
    y0, y1 = imaginary_range

    realAxis = np.linspace(x0, x1, density)
    imaginaryAxis = np.linspace(y0, y1, density)

    # 2-D array to represent mandelbrot atlas
    atlas = np.empty((density, density))

    # color each point in the atlas depending on the iteration count
    for i, ix in enumerate(realAxis):
        for j, iy in enumerate(imaginaryAxis):
            c = complex(ix, iy)
            atlas[i, j] = countIterationsUntilDivergent(c, threshold)
        
        emit_function(atlas[i])
        
    return atlas.T
