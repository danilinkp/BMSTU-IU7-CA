from point import Point
from io_tools import read_matrix
from newton_interpolation import interpolate_3d_newton

function = read_matrix("data/data.txt")

print(interpolate_3d_newton(1.5, 1.5, 1.5, 4, 4, 4, function))
