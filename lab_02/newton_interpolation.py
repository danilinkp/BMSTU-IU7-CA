import numpy as np

from point import Point

from typing import List

type Points = List[Point]


def interpolate_newton(x_value: float, n: int, data: Points) -> float:
    index = find_index(x_value, data)
    work_points = select_points(index, n, data)
    diffs = newton_divided_diffs(work_points)

    return interpolate_value(x_value, diffs[0][1:], work_points)


def interpolate_value(x_value: float, diffs: list, data: Points) -> float:
    n = len(data)
    result = diffs[n - 1]
    for i in range(n - 2, -1, -1):
        result = result * (x_value - data[i].x) + diffs[i]

    return result


def newton_divided_diffs(data: Points) -> list:
    n = len(data)
    newton_table = [[point.x for point in data], [point.y for point in data]]

    for i in range(1, n):
        newton_table.append([0] * n)
        for j in range(n - i):
            newton_table[i + 1][j] = (newton_table[i][j + 1] - newton_table[i][j]) / (data[j + i].x - data[j].x)

    return list(zip(*newton_table))


def select_points(index: int, n: int, data: Points) -> Points:
    length = len(data)
    if length <= n + 1:
        return data

    start = max(0, index - n // 2)
    end = start + n + 1

    if end > length:
        end = length
        start = end - (n + 1)

    return data[start:end]


def find_index(x_value: float, data: Points) -> int:
    if x_value < data[0].x:
        return 0
    elif x_value > data[-1].x:
        return len(data) - 1
    for i in range(len(data) - 1):
        if data[i].x < x_value < data[i + 1].x:
            return i

    return [point.x for point in data].index(x_value)


def interpolate_3d_newton(x: float, y: float, z: float, nx: int, ny: int, nz: int, data: np.ndarray) -> float:
    x_vals = [0, 1, 2, 3, 4]
    y_vals = [0, 1, 2, 3, 4]
    z_vals = [0, 1, 2, 3, 4]

    f_yz = {}
    for k in range(len(z_vals)):
        for j in range(len(y_vals)):
            points_x = [Point(x_vals[i], float(data[k, j, i])) for i in range(len(x_vals))]
            f_yz[(j, k)] = interpolate_newton(x, nx, points_x)

    f_z = {}
    for k in range(len(z_vals)):
        points_y = [Point(y_vals[j], f_yz[(j, k)]) for j in range(len(y_vals))]
        f_z[k] = interpolate_newton(y, ny, points_y)

    points_z = [Point(z_vals[k], f_z[k]) for k in range(len(z_vals))]
    result = interpolate_newton(z, nz, points_z)

    return result
