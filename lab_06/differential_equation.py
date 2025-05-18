import numpy as np


def solve_boundary_problem(alpha, beta, gamma, N=100):
    h = 1.0 / N

    x = np.linspace(0, 1, N + 1)

    a = np.zeros(N + 1)
    b = np.zeros(N + 1)
    c = np.zeros(N + 1)
    d = np.zeros(N + 1)

    for i in range(1, N):
        x_i = x[i]

        a[i] = 1 / h ** 2 + x_i ** 2 / h
        b[i] = -2 / h ** 2 + 4
        c[i] = 1 / h ** 2 - x_i ** 2 / h
        d[i] = 2 * x_i + np.exp(-x_i)

    b[0] = -2 / h ** 2 + 4
    c[0] = 2 / h ** 2
    d[0] = 2 * 0 + np.exp(0) + 2 * alpha / h

    a[N] = 2 / h ** 2
    b[N] = -2 / h ** 2 + 4 - 2 * beta / h
    d[N] = 2 * 1 + np.exp(-1) + 2 * gamma / h

    alpha_coeff = np.zeros(N + 1)
    beta_coeff = np.zeros(N + 1)

    alpha_coeff[0] = -c[0] / b[0]
    beta_coeff[0] = d[0] / b[0]

    for i in range(1, N + 1):
        denom = b[i] + a[i] * alpha_coeff[i - 1]
        alpha_coeff[i] = -c[i] / denom
        beta_coeff[i] = (d[i] - a[i] * beta_coeff[i - 1]) / denom

    u = np.zeros(N + 1)
    u[N] = beta_coeff[N]

    for i in range(N - 1, -1, -1):
        u[i] = alpha_coeff[i] * u[i + 1] + beta_coeff[i]

    return x, u
