from point import Points


class Newton:
    def __init__(self, data: Points) -> None:
        self.data = data
        self.work_points = []
        self.diffs = []

    def find_index(self, x_value: float) -> int:
        if x_value < self.data[0].x:
            return 0
        elif x_value > self.data[-1].x:
            return len(self.data) - 1
        for i in range(len(self.data) - 1):
            if self.data[i].x < x_value < self.data[i + 1].x:
                return i

        return [point.x for point in self.data].index(x_value)

    def select_points(self, index: int, n: int) -> None:
        length = len(self.data)
        if length <= n + 1:
            self.work_points = self.data

        start = max(0, index - n // 2)
        end = start + n + 1

        if end > length:
            end = length
            start = end - (n + 1)

        self.work_points = self.data[start:end]

    def newton_divided_diffs(self) -> None:
        n = len(self.work_points)
        newton_table = [[point.x for point in self.work_points], [point.y for point in self.work_points]]

        for i in range(1, n):
            newton_table.append([0] * n)
            for j in range(n - i):
                newton_table[i + 1][j] = (newton_table[i][j + 1] - newton_table[i][j]) / (
                        self.work_points[j + i].x - self.work_points[j].x)

        self.diffs = list(zip(*newton_table))

    def calc_polynom(self, x_value: float) -> float:
        n = len(self.work_points)
        result = self.diffs[n - 1]
        for i in range(n - 2, -1, -1):
            result = result * (x_value - self.work_points[i].x) + self.diffs[i]

        return result

    def interpolate(self, x_value: float, n: int) -> float:
        index = self.find_index(x_value)
        self.select_points(index, n)
        self.newton_divided_diffs()
        self.diffs = self.diffs[0][1:]

        return self.calc_polynom(x_value)
