import numpy as np
from matplotlib import pyplot as plt

from point import *
from matrix import matrix_sle_solution


def get_approximation_coeffs(data: Points, n: int) -> List[List[float]]:
    # Матрица СЛАУ
    matrix_sle = [[0.0 for i in range(n + 2)] for j in range(n + 1)]

    for i in range(n + 1):
        for j in range(n + 1):
            matrix_sle[i][j] = sum([point.p * point.x ** (i + j) for point in data])

        matrix_sle[i][n + 1] = sum([point.p * point.y * point.x ** i for point in data])

    return matrix_sle


def least_squares_one_dimensional(x: float, data: Points, n: int) -> float:
    matrix_of_coefficients = get_approximation_coeffs(data, n)
    # print(matrix_of_coefficients)
    a_coefs = matrix_sle_solution(matrix_of_coefficients)
    # print(a_coefs)

    phi = sum([a_coefs[i] * x ** i for i in range(len(a_coefs))])

    return phi


def get_approximation_coeffs_2d(data: List[Point], n: int) -> List[List[float]]:
    terms = [(i, j) for i in range(n + 1) for j in range(n + 1) if i + j <= n]
    m = len(terms)

    # Матрица СЛAУ
    matrix_sle = [[0.0 for _ in range(m + 1)] for _ in range(m)]

    # Заполняем матрицу
    for row, (i1, j1) in enumerate(terms):
        for col, (i2, j2) in enumerate(terms):
            matrix_sle[row][col] = sum(point.p * point.x ** (i1 + i2) * point.y ** (j1 + j2) for point in data)
        matrix_sle[row][m] = sum(point.p * point.z * point.x ** i1 * point.y ** j1 for point in data)

    return matrix_sle


def least_squares_two_dimensional(x: float, y: float, data: List[Point], n: int) -> float:
    matrix_of_coefficients = get_approximation_coeffs_2d(data, n)

    a_coefs = matrix_sle_solution(matrix_of_coefficients)

    terms = [(i, j) for i in range(n + 1) for j in range(n + 1) if i + j <= n]

    phi = sum(a_coefs[k] * x ** i * y ** j for k, (i, j) in enumerate(terms))

    return phi


def plot_1d_approximation(data: List[Point], n: int, color: str, label: str, is_empty=True) -> None:
    x_data = np.array([point.x for point in data])
    y_data = np.array([point.y for point in data])

    x_curve = np.linspace(min(x_data), max(x_data), 100)
    y_curve = np.array([least_squares_one_dimensional(x, data, n) for x in x_curve])

    if is_empty:
        plt.figure()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.scatter(x_data, y_data, c='r', label='Исходные точки', s=50)

    plt.plot(x_curve, y_curve, color=color, label=label)
    plt.legend()
    plt.grid(True)


def plot_2d_approximation(data: List[Point], n: int, color: str, label: str, is_empty=True) -> None:
    x_data = np.array([point.x for point in data])
    y_data = np.array([point.y for point in data])
    z_data = np.array([point.z for point in data])

    x_grid = np.linspace(min(x_data), max(x_data), 100)
    y_grid = np.linspace(min(y_data), max(y_data), 100)
    X, Y = np.meshgrid(x_grid, y_grid)
    Z = np.array([[least_squares_two_dimensional(x, y, data, n) for x in x_grid] for y in y_grid])

    if is_empty:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.scatter(x_data, y_data, z_data, c='r', label='Исходные точки', s=50)
    else:
        fig = plt.gcf()
        ax = fig.gca()

    ax.plot_surface(X, Y, Z, cmap=color, alpha=0.7, label=label)
    ax.legend()
