def bisection_method(function: callable, x_start: float, x_end, y: float, max_iter=10, eps: float = 1e-6) -> float:
    if x_start >= x_end:
        raise ValueError("x_start должен быть меньше x_end")

    f_start = function(x_start) - y

    for i in range(1, max_iter + 1):
        x_mid = (x_start + x_end) / 2
        f_mid = function(x_mid) - y

        if abs(f_mid) < eps or i == max_iter:
            return x_mid
        elif f_start * f_mid < 0:
            x_end = x_mid
        else:
            x_start = x_mid

    raise ValueError("Для заданной точности и количества итераций не удалось найти корень")