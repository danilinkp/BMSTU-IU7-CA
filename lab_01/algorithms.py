from typing import Optional, List


class InterpolationPoint:
    def __init__(self, x: float, y: float, derivative: Optional[float] = None,
                 second_derivative: Optional[float] = None) -> None:
        self.x = x
        self.y = y
        self.derivative = derivative
        self.second_derivative = second_derivative


def find_index(x_value: float, data: List[InterpolationPoint]) -> int:
    if x_value < data[0].x:
        return 0
    elif x_value > data[-1].x:
        return len(data) - 1
    for i in range(len(data) - 1):
        if data[i].x < x_value < data[i + 1].x:
            return i


def select_points(index: int, n: int, data: List['InterpolationPoint']) -> List['InterpolationPoint']:
    length = len(data)
    if length <= n + 1:
        return data

    start = max(0, index - n // 2)
    end = start + n + 1

    if end > length:
        end = length
        start = end - (n + 1)

    return data[start:end]


def divided_diffs(data: List['InterpolationPoint']) -> list:
    n = len(data)
    coefs = [data[i].y for i in range(n)]

    for j in range(1, n):  # Для каждого уровня разделенных разностей
        for i in range(n - 1, j - 1, -1):  # Обратный проход
            coefs[i] = (coefs[i] - coefs[i - 1]) / (data[i].x - data[i - j].x)

    return coefs


def interpolate_value(x_value: float, data: List['InterpolationPoint']) -> float:
    diffs = divided_diffs(data)
    n = len(data)
    result = diffs[n - 1]
    for i in range(n - 2, -1, -1):
        result = result * (x_value - data[i].x) + diffs[i]
    return result


def interpolate_newton(x_value: float, n: int, data: List['InterpolationPoint']) -> float:
    index = find_index(x_value, data)

    work_points = select_points(index, n, data)
    return interpolate_value(x_value, work_points)


# data = [
#     InterpolationPoint(-0.5, 0.707),
#     InterpolationPoint(-0.25, 0.924),
#     InterpolationPoint(0.0, 1.0),
#     InterpolationPoint(0.25, 0.924),
#     InterpolationPoint(0.5, 0.707),
#     InterpolationPoint(0.75, 0.383),
#     InterpolationPoint(1.0, 0.0)
# ]
#
# x_value = 0.6  # Значение для интерполяции
# n = 4  # Степень полинома
#
# result = interpolate_newton(x_value, n, data)
# print(f"Интерполированное значение y({x_value}) = {result}")
