from typing import Dict, Tuple, List

from newton_interpolation import Newton, Point


def interpolate_newton_2d(x: float, y: float,
                          table_data: Dict[Tuple[float, float], float],
                          x_points: List[float],
                          y_points: List[float],
                          degree_x: int = 2,
                          degree_y: int = 2) -> float:
    temp_results = {}

    for x_val in x_points:
        points_y = [Point(y_val, table_data[(x_val, y_val)])
                    for y_val in y_points
                    if (x_val, y_val) in table_data]

        if len(points_y) > degree_y:
            newton_y = Newton(points_y)
            temp_results[x_val] = newton_y.interpolate(y, degree_y)


    points_x = [Point(x_val, z) for x_val, z in temp_results.items()]
    newton_x = Newton(points_x)
    return newton_x.interpolate(x, degree_x)