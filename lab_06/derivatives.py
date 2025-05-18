def one_side_derivative(y_0: float, y_1: float, h: float = 1) -> float:
    return (y_1 - y_0) / h


def central_derivative(y_0: float, y_2: float, h: float = 1) -> float:
    return (y_2 - y_0) / 2 * h


def second_runge_formula(y_0: float, y_1: float, y_2: float, h: float = 1) -> float:
    first_elem = one_side_derivative(y_0, y_1, h)
    second_elem = one_side_derivative(y_1, y_2, h)

    return 2 * first_elem - second_elem


def derivative_with_alignment(y_0: float, y_1: float, x_0: float, x_1: float) -> float:
    eta_0 = 1 / y_0
    eta_1 = 1 / y_1

    ksi_0 = 1 / x_0
    ksi_1 = 1 / x_1

    delta_eta = eta_1 - eta_0
    delta_ksi = ksi_1 - ksi_0

    k = delta_eta / delta_ksi if delta_ksi != 0 else 0

    return k * (y_0 ** 2) / (x_0 ** 2)


def second_derivative(y_0: float, y_1: float, y_2: float, h: float = 1) -> float:
    return (y_0 - 2 * y_1 + y_2) / h ** 2
