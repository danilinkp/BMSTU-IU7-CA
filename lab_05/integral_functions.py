import numpy as np
from typing import Tuple


def trapezoid_method(function: callable, x_start: float, x_end: float, n: int) -> float:
    h = (x_end - x_start) / n

    result = 0
    for i in range(n):
        x_i = x_start + i * h
        x_i1 = x_i + h

        result += h * (function(x_i) + function(x_i1)) / 2

    return result


def simpson_method(function: callable, x_start: float, x_end: float, n: int) -> float:
    if n % 2 != 0:
        raise ValueError("n must be even")

    h = (x_end - x_start) / n

    result = function(x_start) + function(x_end)

    for i in range(1, n):
        x = x_start + i * h
        if i % 2 == 0:
            result += 2 * function(x)
        else:
            result += 4 * function(x)

    result *= h / 3

    return result


def legendre_roots(n: int, eps: float = 1e-12, max_iters: int = 100) -> Tuple[np.ndarray, np.ndarray]:
    roots = np.zeros(n)
    weights = np.zeros(n)
    m = (n + 1) // 2

    for k in range(1, m + 1):
        x = np.cos(np.pi * (2 * k - 1) / (2 * n))

        for _ in range(max_iters):
            P, dP = legendre_polynomial(n, x)
            dx = P / dP
            x -= dx
            if abs(dx) < eps:
                break
        else:
            print(f"Предупреждение: метод Ньютона не сошелся для k={k}")

        idx = m - k
        roots[idx] = -x
        roots[n - 1 - idx] = x
        weight = 2.0 / ((1.0 - x ** 2) * dP ** 2)
        weights[idx] = weight
        weights[n - 1 - idx] = weight

    if n % 2:
        _, dP = legendre_polynomial(n, 0.0)
        roots[m - 1] = 0.0
        weights[m - 1] = 2.0 / (dP ** 2)

    return roots, weights


def legendre_polynomial(n: int, x: float) -> Tuple[float, float]:
    if n == 0:
        return 1.0, 0.0

    P_km1, P_k = 1.0, x
    for k in range(1, n):
        P_kp1 = ((2 * k + 1) * x * P_k - k * P_km1) / (k + 1)
        P_km1, P_k = P_k, P_kp1

    if abs(x) < 1 - 1e-10:
        P_prime = (n * P_km1 - n * x * P_k) / (1 - x ** 2)
    else:
        sign = 1 if x > 0 else (-1) ** (n + 1)
        P_prime = sign * n * (n + 1) / 2

    return P_k, P_prime


def gauss_method(function: callable, x_start: float, x_end: float, n: int) -> float:
    roots, weights = legendre_roots(n)

    a, b = x_start, x_end
    scale = (b - a) / 2
    shift = (a + b) / 2
    transformed_roots = scale * roots + shift

    result = scale * np.sum(weights * function(transformed_roots))

    return result

