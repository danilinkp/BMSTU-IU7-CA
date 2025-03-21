import numpy as np
from scipy.linalg import solve


def get_polynom(x, n: int, coeffs: list) -> float:
    """Вычисляет значение полинома y(x) = (1 - x) + c1 x (1-x) + c2 x^2 (1-x) + ..."""
    result = 1 - x  # u_0(x)
    for k in range(1, n + 1):
        result += coeffs[k - 1] * x ** k * (1 - x)
    return result


def solve_ode_least_squares(n: int, num_points: int = 100):
    """Решает y'' + x y' + y = 2x с y(0) = 1, y(1) = 0 методом наименьших квадратов."""
    x = np.linspace(0, 1, num_points)

    # Базисные функции и их производные
    basis = []
    basis_prime = []
    basis_double = []
    for k in range(1, n + 1):
        u = x ** k * (1 - x)
        u_prime = k * x ** (k - 1) * (1 - x) - x ** k
        u_double = k * (k - 1) * x ** (k - 2) * (1 - x) - 2 * k * x ** (k - 1) if k >= 2 else -2 * np.ones_like(x)
        basis.append(u)
        basis_prime.append(u_prime)
        basis_double.append(u_double)

    # Невязка для u_0(x) = 1 - x
    u0_double = 0
    u0_prime = -1 * np.ones_like(x)
    u0 = 1 - x
    base_residual = u0_double + x * u0_prime + u0 - 2 * x  # 1 - 4x

    # Вычисление L u_k = u_k'' + x u_k' + u_k
    L = [basis_double[k] + x * basis_prime[k] + basis[k] for k in range(n)]

    # Матрица A и вектор b для МНК
    A = np.zeros((n, n))
    b = np.zeros(n)
    for i in range(n):
        for j in range(n):
            A[i, j] = np.sum(L[i] * L[j]) / num_points  # Скалярное произведение
        b[i] = -np.sum(L[i] * base_residual) / num_points  # Проекция на базис

    coeffs = solve(A, b)
    return coeffs


def evaluate_solution(x_values, n: int, coeffs: list):
    """Вычисляет y(x) для заданных x."""
    return np.array([get_polynom(x, n, coeffs) for x in x_values])
