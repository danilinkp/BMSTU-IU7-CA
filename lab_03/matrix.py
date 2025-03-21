from point import *


def matrix_to_triangle_view(matrix: List[List[float]]) -> List[List[float]]:
    n = len(matrix)
    for k in range(n):
        for i in range(k + 1, n):
            coeff = -(matrix[i][k] / matrix[k][k])
            for j in range(k, n + 1):
                matrix[i][j] += coeff * matrix[k][j]

    # print(matrix)
    return matrix


def matrix_sle_solution(matrix: List[List[float]]) -> Optional[List[float]]:
    # print(matrix)
    n = len(matrix)
    if n == 0:
        return None

    matrix = matrix_to_triangle_view(matrix)
    if matrix is None:
        return None
    result = [0.0] * n
    for i in range(n - 1, -1, -1):
        sum_ax = sum(matrix[i][j] * result[j] for j in range(i + 1, n))
        result[i] = (matrix[i][n] - sum_ax) / matrix[i][i]  # n — индекс b

    # result = [0.0 for _ in range(n)]
    # for i in range(n - 1, -1, -1):
    #     for j in range(n - 1, i, -1):
    #         matrix[i][n] -= result[j] * matrix[i][j]
    #     result.append(matrix[i][n] / matrix[i][i])

    return result
