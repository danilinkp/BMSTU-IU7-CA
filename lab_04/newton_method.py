import numpy as np


def newton_method(function: callable, jacobi: callable, x0: np.ndarray, eps: float = 1e-6,
                  max_iter: int = 30) -> np.ndarray:
    x = x0.copy()
    iter_count = 0

    while iter_count < max_iter:
        f_x = function(x)

        if np.linalg.norm(f_x) < eps:
            return x

        J = jacobi(x)

        delta = np.linalg.solve(J, -f_x)

        x = x + delta

        iter_count += 1

    raise ValueError("Метод Ньютона не сошелся за максимальное число итераций")
