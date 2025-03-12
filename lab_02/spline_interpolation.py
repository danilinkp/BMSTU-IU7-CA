from typing import List
from point import Point, Points


class Spline:
    def __init__(self, data: Points):
        self.data = data
        self.n = len(data) - 1
        self.a = [point.y for point in data[:-1]]
        self.b = [0.0] * self.n
        self.c = [0.0] * (self.n + 1)
        self.d = [0.0] * self.n
        self.compute_coefficients()

    def compute_coefficients(self):
        # Вычисляем шаги h
        h = [self.data[i + 1].x - self.data[i].x for i in range(self.n)]

        # Решаем трёхдиагональную систему для вторых производных
        alpha = [0.0] * (self.n + 1)
        l = [0.0] * (self.n + 1)
        mu = [0.0] * (self.n + 1)
        z = [0.0] * (self.n + 1)

        l[0] = 1.0
        mu[0] = 0.0
        z[0] = 0.0

        for i in range(1, self.n):
            alpha[i] = 3 * ((self.data[i + 1].y - self.data[i].y) / h[i] -
                            (self.data[i].y - self.data[i - 1].y) / h[i - 1])
            l[i] = 2 * (self.data[i + 1].x - self.data[i - 1].x) - h[i - 1] * mu[i - 1]
            mu[i] = h[i] / l[i]
            z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]

        l[self.n] = 1.0
        z[self.n] = 0.0
        self.c[self.n] = 0.0

        for i in range(self.n - 1, -1, -1):
            self.c[i] = z[i] - mu[i] * self.c[i + 1]
            self.b[i] = ((self.data[i + 1].y - self.data[i].y) / h[i] -
                         h[i] * (self.c[i + 1] + 2 * self.c[i]) / 3)
            self.d[i] = (self.c[i + 1] - self.c[i]) / (3 * h[i])

    def evaluate(self, x_val: float) -> float:
        # Находим интервал
        if x_val <= self.data[0].x:
            i = 0
            dx = x_val - self.data[0].x
        elif x_val >= self.data[-1].x:
            i = self.n - 1
            dx = x_val - self.data[i].x
        else:
            for i in range(self.n):
                if self.data[i].x <= x_val < self.data[i + 1].x:
                    dx = x_val - self.data[i].x
                    break
            else:
                i = self.n - 1
                dx = x_val - self.data[i].x

        return self.a[i] + self.b[i] * dx + self.c[i] * dx ** 2 + self.d[i] * dx ** 3