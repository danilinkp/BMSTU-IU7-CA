# from algorithms import InterpolationPoint, Points
# from algorithms import interpolate_newton, interpolate_hermite
# from algorithms import generate_table, print_points, print_hermite_div_diffs, print_newton_div_diffs
# from algorithms import reverse_data, find_root_by_newton, find_root_by_hermite
#
# FILEPATH = "data/data.txt"
#
#
# def read_points(file: str) -> Points:
#     data = []
#     with open(file=file, mode="rt") as f:
#         for line in f.readlines():
#             points = list(map(float, line.split()))
#             if len(points) == 3:
#                 point = InterpolationPoint(points[0], points[1], points[2])
#             elif len(points) >= 4:
#                 point = InterpolationPoint(points[0], points[1], points[2], points[3])
#             else:
#                 point = InterpolationPoint(points[0], points[1])
#             data.append(point)
#     return data
#
#
# def main() -> None:
#     x_value = float(input("Введите значение x: "))
#     n = int(input("Введите n: "))
#
#     n2 = int(input("Введите кол-во узлов для полинома Эрмита: "))
#
#     data = read_points(FILEPATH)
#
#     print_newton_div_diffs(x_value, n, data)
#     print_hermite_div_diffs(x_value, n2 - 1, data)
#
#     print(f"Интерполяция полиномом Ньютона: {interpolate_newton(x_value, n, data)}")
#     print(f"Интерполяция полиномом Эрмита: {interpolate_hermite(x_value, n2 - 1, data)}")
#     print("---------------\n")
#
#     generate_table(data, x_value, 5)
#     print("\n")
#
#     root_by_newton = find_root_by_newton(data)
#     root_by_hermite = find_root_by_hermite(data)
#     print(f"Корень табличной функции с помощью обратной интерполяции полином Ньютона: {root_by_newton}")
#     print(f"Корень табличной функции с помощью обратной интерполяции полином Эрмита: {root_by_hermite}\n")
#
#     print("Решение системы нелинейных уравнений")
#     data_func_1_y_x = read_points("data/func_y_x.txt")
#     data_func_2_x_y = read_points("data/func_x_y.txt")
#
#     n = 4
#     func_1_x_y = reverse_data(data_func_1_y_x)
#
#     new_data_solve: Points = []
#     for i, point in enumerate(data_func_2_x_y):
#         f1_x = point.y
#         f2_inv_x = interpolate_newton(point.x, n, func_1_x_y)
#         f_x = f1_x - f2_inv_x
#         new_data_solve.append(InterpolationPoint(point.x, f_x))
#
#     print_points(new_data_solve)
#
#     solve_1 = find_root_by_newton(new_data_solve, n)
#     print(f"Решение системы: x = {solve_1:.6f}")
#
#
# if __name__ == "__main__":
#     main()
class TuringMachine:
    def __init__(self, tape, blank='_'):
        self.tape = list(tape) + [blank]  # Добавляем пустой символ в конец ленты
        self.blank = blank
        self.head = 0
        self.state = 'q0'
        self.transitions = {
            ('q0', '1'): ('q0', '1', 'R'),
            ('q0', '0'): ('q0', '0', 'R'),
            ('q0', '_'): ('q1', '_', 'L'),
            ('q1', '1'): ('q2', '_', 'L'),
            ('q1', '0'): ('q3', '_', 'L'),
            ('q2', '_'): ('q4', '1', 'R'),
            ('q3', '_'): ('q5', '_', 'R'),
            ('q4', '_'): ('q6', '1', 'R'),
            ('q6', '_'): ('qf', '_', 'N')  # Финальное состояние
        }

    def step(self):
        char = self.tape[self.head]
        if (self.state, char) in self.transitions:
            new_state, new_char, move = self.transitions[(self.state, char)]
            self.tape[self.head] = new_char
            self.state = new_state
            if move == 'R':
                self.head += 1
            elif move == 'L':
                self.head -= 1

    def run(self):
        while self.state != 'qf':
            self.step()
        return ''.join(c for c in self.tape if c != self.blank)


# Входное двоичное число (например, 101 = 5 в десятичной системе)
binary_number = "101"

# Запускаем машину Тьюринга
tm = TuringMachine(binary_number)
unary_output = tm.run()
print("Унарное представление:", unary_output)
