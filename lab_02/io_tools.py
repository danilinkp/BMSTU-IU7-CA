import numpy as np


def read_matrix(filename: str) -> np.ndarray:
    data = []
    current_table = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                if current_table:
                    data.append(current_table)
                    current_table = []
                continue

            if line.startswith('z='):
                continue
            elif line.startswith('y\\x'):
                continue

            values = [float(x) for x in line.split()[1:]]
            current_table.append(values)

        if current_table:
            data.append(current_table)

    return np.array(data)
