import numpy as np

def is_numpy(obj) -> bool:
    return type(obj).__module__ == np.__name__

def round_coord(coordinate: tuple, decimal_place) -> tuple[float, float]:
    x = coordinate[0].item() if is_numpy(coordinate[0]) else coordinate[0]
    y = coordinate[1].item() if is_numpy(coordinate[0]) else coordinate[1]

    return round(x, decimal_place), round(y, decimal_place)