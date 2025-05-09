from typing import Tuple, Dict, List


def read_function(filename: str) -> Tuple[Dict[Tuple[float, float], float], List[float], List[float]]:
    z = dict()
    with open(filename, mode="r", encoding="utf8") as f:
        x = list(map(float, f.readline().split()[1:]))
        y = []
        data = f.readlines()
        for line in data:
            y_i = float(line.split()[0])
            y.append(y_i)
            f = list(map(float, line.split()[1:]))
            for i in range(len(x)):
                z[(x[i], y_i)] = f[i]

    return z, x, y
