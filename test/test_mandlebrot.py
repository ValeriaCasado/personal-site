import pytest
import numpy as np

from project.mandlebrot import get_new_range, mandlebrot
from .test_helpers import round_coord

R = (-2.25, 0.75)
I = (-1.5, 1.5)
density = 1000


def test_get_mandlebrot_range():

    realAxis = np.linspace(R[0], R[1], density)
    imaginaryAxis = np.linspace(I[0], I[1], density)

    x_ = realAxis[450].item(), realAxis[550].item()
    y_ = imaginaryAxis[450].item(), imaginaryAxis[550].item()

    x, y = get_new_range(
        real_range=R, 
        imaginary_range=I, 
        coord=(500, 500), 
        density=1000)
    
    assert round_coord(x, 3) == round_coord(x_, 3)
    assert round_coord(y, 3) == round_coord(y_, 3)


def test_mandlebrot_function():
    a = mandlebrot()

    assert len(a) == 1000
    assert len(a[0]) == 1000