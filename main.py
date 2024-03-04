from ucs import *

# Route points
start = [6, 6]
end = [3, 3]

matrix = np.array([
    [8, 9, 9, 9, 9, 3, 9, 6, 7, 8],
    [8, 9, Z, Z, Z, 3, 9, 6, 7, 8],
    [6, 9, Z, 6, 5, 3, 8, 5, 7, 8],
    [7, 9, Z, 2, 4, 3, 8, 7, 5, 8],
    [Z, Z, Z, Z, Z, 3, Z, Z, Z, Z],
    [9, 9, Z, 8, 3, 9, 9, Z, 8, 9],
    [9, 9, Z, 9, 3, 4, 2, Z, 7, 7],
    [9, 9, Z, 9, 3, Z, Z, Z, 8, 7],
    [9, 9, 9, 9, 3, 9, 8, 7, 7, 8],
    [9, 9, 7, 6, 3, 7, 9, 8, 9, 9]
])

# Do UCS
checker = ucs(matrix, start, end)

if checker is False:
    print("No path found")
