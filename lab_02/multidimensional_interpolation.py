import numpy as np

from typing import Optional
from point import Point
from newton_interpolation import Newton
from spline_interpolation import Spline


def interpolate_x(x: float, data: np.ndarray, f_yz: dict, interp_type: str, nx: Optional[int]):
    x_vals = [0, 1, 2, 3, 4]
    y_vals = [0, 1, 2, 3, 4]
    z_vals = [0, 1, 2, 3, 4]

    for k in range(len(z_vals)):
        for j in range(len(y_vals)):
            points_x = [Point(x_vals[i], float(data[k, j, i])) for i in range(len(x_vals))]
            if interp_type == "newton":
                newton_x = Newton(points_x)
                f_yz[(j, k)] = newton_x.interpolate(x, nx)
            else:
                spline_x = Spline(points_x)
                f_yz[(j, k)] = spline_x.evaluate(x)


def interpolate_y(y: float, f_z: dict, f_yz: dict, interp_type: str, ny: Optional[int]):
    y_vals = [0, 1, 2, 3, 4]
    z_vals = [0, 1, 2, 3, 4]

    for k in range(len(z_vals)):
        points_y = [Point(y_vals[j], f_yz[(j, k)]) for j in range(len(y_vals))]
        if interp_type == "newton":
            newton_y = Newton(points_y)
            f_z[k] = newton_y.interpolate(y, ny)
        else:
            spline_y = Spline(points_y)
            f_z[k] = spline_y.evaluate(y)


def interpolate_z(z: float, f_z: dict, interp_type: str, nz: Optional[int]) -> float:
    z_vals = [0, 1, 2, 3, 4]

    points_z = [Point(z_vals[k], f_z[k]) for k in range(len(z_vals))]
    if interp_type == "newton":
        newton_z = Newton(points_z)
        result = newton_z.interpolate(z, nz)
    else:
        spline_z = Spline(points_z)
        result = spline_z.evaluate(z)

    return result


def interpolate_3d_newton(args: list[float], degrees: list[int], data: np.ndarray) -> float:
    x, y, z = args
    nx, ny, nz = degrees

    f_yz = {}
    interpolate_x(x, data, f_yz, interp_type="newton", nx=nx)

    f_z = {}
    interpolate_y(y, f_z, f_yz, interp_type="newton", ny=ny)

    result = interpolate_z(z, f_z, interp_type="newton", nz=nz)

    return result


def interpolate_3d_spline(args: list[float], data: np.ndarray) -> float:
    x, y, z = args

    f_yz = {}
    interpolate_x(x, data, f_yz, interp_type="spline", nx=None)

    f_z = {}
    interpolate_y(y, f_z, f_yz, interp_type="spline", ny=None)

    result = interpolate_z(z, f_z, interp_type="spline", nz=None)

    return result


def mixed_interpolation(args: list[float], degrees: list[int], data: np.ndarray,
                        types_of_interpolation: list[str]) -> float:
    first_type = types_of_interpolation[0]
    second_type = types_of_interpolation[1]
    third_type = types_of_interpolation[2]

    x, y, z = args
    nx, ny, nz = degrees

    f_yz = {}
    interpolate_x(x, data, f_yz, interp_type=first_type, nx=nx)

    f_z = {}
    interpolate_y(y, f_z, f_yz, interp_type=second_type, ny=ny)

    result = interpolate_z(z, f_z, interp_type=third_type, nz=nz)

    return result
