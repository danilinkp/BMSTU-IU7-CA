from typing import Dict, Tuple, List

from integral_functions import simpson_method, gauss_method
from twodimensional_interpolation import interpolate_newton_2d


def integrate_y(x: float, table: Dict[Tuple[float, float], float], x_points: List[float],
                y_points: List[float], phi: callable, psi: callable, method: str = 'simpson', n: int = 10) -> float:
    y_lower = phi(x)
    y_upper = psi(x)

    if y_lower >= y_upper:
        return 0.0

    def f(y: float) -> float:
        return interpolate_newton_2d(x, y, table, x_points, y_points)

    if method == 'simpson':
        return simpson_method(f, y_lower, y_upper, n)
    else:
        return gauss_method(f, y_lower, y_upper, n)


def double_integral(table: Dict[Tuple[float, float], float], x_points: List[float], y_points: List[float],
                    a: float, b: float, phi: callable, psi: callable,
                    x_method: str = 'simpson', y_method: str = 'simpson',
                    x_points_num: int = 10, y_points_num: int = 10) -> float:
    def g(x: float) -> float:
        return integrate_y(x, table, x_points, y_points, phi, psi, y_method, y_points_num)

    if x_method == 'simpson':
        return simpson_method(g, a, b, x_points_num)
    else:
        return gauss_method(g, a, b, x_points_num)
