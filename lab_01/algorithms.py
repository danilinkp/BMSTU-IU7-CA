from typing import Optional, List
from prettytable import PrettyTable

type Points = List[InterpolationPoint]


class InterpolationPoint:
    def __init__(self, x: float, y: float, derivative: Optional[float] = None,
                 second_derivative: Optional[float] = None) -> None:
        self.x = x
        self.y = y
        self.derivative = derivative
        self.second_derivative = second_derivative


def interpolate_newton(x_value: float, n: int, data: Points) -> float:
    index = find_index(x_value, data)
    work_points = select_points(index, n, data)
    diffs = newton_divided_diffs(work_points)

    return interpolate_value(x_value, diffs[0][1:], work_points)


def interpolate_hermite(x_value: float, n: int, data: Points, max_derivative_order: int = 2) -> float:
    index = find_index(x_value, data)
    work_points = select_points(index, n, data)
    hermite_points = prepare_hermite_points(work_points, max_derivative_order)
    diffs = hermite_divided_diffs(hermite_points)

    return interpolate_value(x_value, diffs[0][1:], hermite_points)


def interpolate_value(x_value: float, diffs: list, data: Points) -> float:
    n = len(data)
    result = diffs[n - 1]
    for i in range(n - 2, -1, -1):
        result = result * (x_value - data[i].x) + diffs[i]

    return result


def prepare_hermite_points(data: Points, max_derivative_order: int) -> Points:
    result = []
    for point in data:
        result.append(InterpolationPoint(point.x, point.y, point.derivative, point.second_derivative))
        if max_derivative_order >= 1 and point.derivative is not None:
            result.append(InterpolationPoint(point.x, point.y, point.derivative, point.second_derivative))
        if max_derivative_order >= 2 and point.second_derivative is not None:
            result.append(InterpolationPoint(point.x, point.y, point.derivative, point.second_derivative))
    return result


def hermite_divided_diffs(data: Points) -> list:
    n = len(data)

    table = [[0.0] * (n + 1) for _ in range(n + 1)]
    table[0] = [point.x for point in data]
    table[1] = [point.y for point in data]

    for j in range(1, n):
        for i in range(n - j):
            if table[0][i + j] == table[0][i]:
                if j == 1 and data[i].derivative is not None:
                    table[j + 1][i] = data[i].derivative
                elif j == 2 and data[i].second_derivative is not None:
                    table[j + 1][i] = data[i].second_derivative / 2
            else:
                table[j + 1][i] = (table[j][i + 1] - table[j][i]) / (table[0][i + j] - table[0][i])

    return list(zip(*table))


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


def generate_table(data: Points, x_value: float, max_degree: int) -> None:
    table = PrettyTable()
    table.align = "r"
    print(f"Таблица значений y({x_value}) для полиномов Ньютона и Эрмита при фиксированном x={x_value}:")
    table.field_names = ["Степень", "Ньютон", "Эрмит"]

    for n in range(1, max_degree + 1):
        newton_result = interpolate_newton(x_value, n, data)
        hermite_result = interpolate_hermite(x_value, n, data)
        table.add_row([n, newton_result, hermite_result])
    table.float_format = '.3'
    print(table)


def reverse_data(data: Points) -> Points:
    reversed_data = []
    for point in data:
        if point.derivative is not None:
            df_dy = 1 / point.derivative
        else:
            df_dy = None

        if point.second_derivative is not None and point.derivative is not None:
            d2f_dy2 = -point.second_derivative / (point.derivative ** 3)
        else:
            d2f_dy2 = None

        reversed_data.append(InterpolationPoint(point.y, point.x, df_dy, d2f_dy2))

    return reversed_data


def find_root_by_newton(data: Points, max_degree: int = 4) -> float:
    reversed_data = reverse_data(data)
    return interpolate_newton(0, max_degree, reversed_data)


def find_root_by_hermite(data: Points, max_degree: int = 4) -> float:
    reversed_data = reverse_data(data)
    return interpolate_hermite(0, max_degree, reversed_data)


def print_points(data: Points) -> None:
    table = PrettyTable(["x", "y"])
    table.align = "r"
    for point in data:
        table.add_row([point.x, point.y])
    table.float_format = '.3'
    print(table)


def print_diffs_tables(data: list) -> None:
    table = PrettyTable()
    headers = ["x", "y"] + [f"Разность {i}" for i in range(len(data) - 1)]

    table.field_names = headers
    table.align = "r"

    for i in range(len(data)):
        row = list(data[i][:len(data) - i + 1]) + [""] * i
        table.add_row(row)

    table.float_format = '.3'
    print(table)


def print_hermite_div_diffs(x_value: float, n: int, data: Points) -> None:
    index = find_index(x_value, data)
    work_points = select_points(index, n, data)
    hermite_points = prepare_hermite_points(work_points, 2)
    diffs = hermite_divided_diffs(hermite_points)

    print_diffs_tables(diffs)


def print_newton_div_diffs(x_value: float, n: int, data: Points) -> None:
    index = find_index(x_value, data)
    work_points = select_points(index, n, data)
    diffs = newton_divided_diffs(work_points)

    print_diffs_tables(diffs)
