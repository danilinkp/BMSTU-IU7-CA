from algorithms import InterpolationPoint, Points
from algorithms import interpolate_newton, interpolate_hermite
from algorithms import generate_table, print_points
from algorithms import reverse_data, find_root_by_newton, find_root_by_hermite

FILEPATH = "data/data.txt"


def read_points(file: str) -> Points:
    data = []
    with open(file=file, mode="rt") as f:
        for line in f.readlines():
            points = list(map(float, line.split()))
            if len(points) == 3:
                point = InterpolationPoint(points[0], points[1], points[2])
            elif len(points) >= 4:
                point = InterpolationPoint(points[0], points[1], points[2], points[3])
            else:
                point = InterpolationPoint(points[0], points[1])
            data.append(point)
    return data


def main() -> None:
    x_value = float(input("Введите значение x: "))
    n = int(input("Введите n: "))

    data = read_points(FILEPATH)

    print(f"Интерполяция полиномом Ньютона: {interpolate_newton(x_value, n, data)}")
    print(f"Интерполяция полиномом Эрмита: {interpolate_hermite(x_value, n, data)}")
    print("---------------\n")

    generate_table(data, x_value, 5)
    print("\n")

    root_by_newton = find_root_by_newton(data)
    root_by_hermite = find_root_by_hermite(data)
    print(f"Корень табличной функции с помощью обратной интерполяции полином Ньютона: {root_by_newton}")
    print(f"Корень табличной функции с помощью обратной интерполяции полином Эрмита: {root_by_hermite}\n")

    print("Решение системы нелинейных уравнений")
    data_func_1_y_x = read_points("data/func_y_x.txt")
    data_func_2_x_y = read_points("data/func_x_y.txt")

    n = 4
    func_1_x_y = reverse_data(data_func_1_y_x)

    new_data_solve: Points = []
    for i, point in enumerate(data_func_2_x_y):
        f1_x = point.y
        f2_inv_x = interpolate_newton(point.x, n, func_1_x_y)
        f_x = f1_x - f2_inv_x
        new_data_solve.append(InterpolationPoint(point.x, f_x))

    print_points(new_data_solve)

    solve_1 = find_root_by_newton(new_data_solve, n)
    print(f"Решение системы: x = {solve_1:.6f}")


if __name__ == "__main__":
    main()
