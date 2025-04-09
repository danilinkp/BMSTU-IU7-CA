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