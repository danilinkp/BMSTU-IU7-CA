from random import randint
from typing import Optional

import numpy as np

from point import Point


def generate_data_1D(function, sx, ex, amount, filename=None):
    data = []
    x_values = np.linspace(sx, ex, amount)

    for x in x_values:
        point = Point(x, function(x), 0, randint(1, 5))
        if filename is not None:
            with open(filename, 'a') as f:
                f.write(f"{point}\n")
        data.append(point)

    return data


def read_data(filename):
    with open(filename) as f:
        data = []
        for line in f:
            d = [float(i) for i in line.split()]
            data.append(Point(d[0], d[1], d[2], d[3]))

    return data


def generate_data_2D(f, sx, ex, sy, ey, amount_x, amount_y, filename=None):
    data = []
    x_values = np.linspace(sx, ex, amount_x)
    y_values = np.linspace(sy, ey, amount_y)

    for i in range(amount_x):
        for j in range(amount_y):
            point = Point(float(x_values[i]), float(y_values[j]), f(x_values[i], y_values[j]), randint(1, 10))
            if filename is not None:
                with open(filename, 'a') as f:
                    f.write(f"{point}\n")
            data.append(point)

    return data

def set_all_weights(data, weight=1):
    for point in data:
        point.p = weight

