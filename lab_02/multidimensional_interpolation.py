import numpy as np

from point import Point
from newton_interpolation import Newton
from spline_interpolation import Spline

def interpolate_3d_newton(x: float, y: float, z: float, nx: int, ny: int, nz: int, data: np.ndarray) -> float:
    x_vals = [0, 1, 2, 3, 4]
    y_vals = [0, 1, 2, 3, 4]
    z_vals = [0, 1, 2, 3, 4]

    f_yz = {}
    for k in range(len(z_vals)):
        for j in range(len(y_vals)):
            points_x = [Point(x_vals[i], float(data[k, j, i])) for i in range(len(x_vals))]
            newton_x = Newton(points_x)
            # f_yz[(j, k)] = interpolate_newton(x, nx, points_x)
            f_yz[(j, k)] = newton_x.interpolate(x, nx)

    f_z = {}
    for k in range(len(z_vals)):
        points_y = [Point(y_vals[j], f_yz[(j, k)]) for j in range(len(y_vals))]
        # f_z[k] = interpolate_newton(y, ny, points_y)
        newton_y = Newton(points_y)
        f_z[k] = newton_y.interpolate(y, ny)

    points_z = [Point(z_vals[k], f_z[k]) for k in range(len(z_vals))]
    newton_z = Newton(points_z)
    result = newton_z.interpolate(z, nz)
    # result = interpolate_newton(z, nz, points_z)

    return result


def interpolate_3d_spline(x: float, y: float, z:float, data: np.ndarray) -> float:
    x_vals = [0, 1, 2, 3, 4]
    y_vals = [0, 1, 2, 3, 4]
    z_vals = [0, 1, 2, 3, 4]

    f_yz = {}
    for k in range(len(z_vals)):
        for j in range(len(y_vals)):
            points_x = [Point(x_vals[i], float(data[k, j, i])) for i in range(len(x_vals))]
            spline_x = Spline(points_x)
            f_yz[(j, k)] = spline_x.evaluate(x)

    f_z = {}
    for k in range(len(z_vals)):
        points_y = [Point(y_vals[j], f_yz[(j, k)]) for j in range(len(y_vals))]
        spline_y = Spline(points_y)
        f_z[k] = spline_y.evaluate(y)

    points_z = [Point(z_vals[k], f_z[k]) for k in range(len(z_vals))]
    spline_z = Spline(points_z)
    result = spline_z.evaluate(z)

    return result

