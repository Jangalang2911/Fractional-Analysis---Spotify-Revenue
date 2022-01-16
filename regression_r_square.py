""" This file is used to calculate the r-square value for the linear regression model, which helps
determine the strength of the association of the model.
"""
import statistics
import main


def find_rsquare_matrix() -> list[list[float, float], list[float, float]]:
    """
    Find R for the spotify_revenue file
    """
    loaded_csv = main.read_spotify_regression_data('spotify_revenue.csv',
                                                   'premium subscribers sportify.csv',
                                                   'Normal users spotify.csv')
    list_of_items = [loaded_csv[item] for item in loaded_csv]
    premium = []
    normal = []
    revenue = []
    for item in list_of_items:
        premium.append(item[1])
        normal.append(item[2])
        revenue.append(item[0])
    avg_x1 = statistics.mean(premium)  # x1 is predictor one
    avg_x2 = statistics.mean(normal)  # x2 is predictor 2
    avg_y = statistics.mean(revenue)  # y is the revenue

    n1, n2, n3, d11, d21, d31, d12, d22, d32 = 0, 0, 0, 0, 0, 0, 0, 0, 0

    # n in the variable stands to refer to the numerator of the correlation function and d stands
    # for the denominator in the correlation function

    for i in range(len(premium)):
        n1 = n1 + (premium[i] - avg_x1) * (revenue[i] - avg_y)
        n2 = n2 + (normal[i] - avg_x2) * (revenue[i] - avg_y)
        n3 = n3 + (normal[i] - avg_x2) * (premium[i] - avg_x1)
        d11 = d11 + (premium[i] - avg_x1) ** 2
        d21 = d21 + (normal[i] - avg_x2) ** 2
        d31 = d31 + (normal[i] - avg_x2) ** 2
        d12 = d12 + (revenue[i] - avg_y) ** 2
        d22 = d22 + (revenue[i] - avg_y) ** 2
        d32 = d32 + (premium[i] - avg_x1) ** 2

    # r stands for correlation

    r1 = n1/((d11 * d12)**0.5)
    r2 = n2/((d21 * d22)**0.5)
    r3 = n3/((d31 * d32)**0.5)

    r1 = r1 ** 2
    r2 = r2 ** 2
    r3 = r3 ** 2

    return [[r1, 0], [r2, r3]]


def r_square(lst: list[tuple[float, float], tuple[float, float]]) -> float:
    """
    Function to find total value for r^square for the whole model
    """
    # the variable name assignment assignment follows the same logic as the one in
    # the above function

    r1 = lst[0][0]
    r2 = lst[1][0]
    r3 = lst[1][1]
    rx1y = r1 ** 0.5
    rx2y = r2 ** 0.5
    rx2x1 = r3 ** 0.5
    transpose = calculate_transpose([[rx1y], [rx2y]])
    inverse = calculate_inverse([[1, rx2x1], [rx2x1, 1]])
    m1 = multiply_matrix(transpose, inverse)
    r2 = multiply_matrix(m1, [[rx1y], [rx2y]])
    return r2[0][0]


def calculate_transpose(lst: list[list[float]]) -> list[list[float]]:
    """This function calculates the transpose of a matrix. Each row in the matrix should be a
    list within the list
    """
    new_row = len(lst)
    new_colowm = len(lst[0])
    transpose_list = []
    for i in range(new_colowm):
        temp_list = []
        transpose_list.append(temp_list)
        for j in range(new_row):
            temp_list.append(lst[j][i])
    return transpose_list


def calculate_inverse(lst: list[list[float, float], list[float, float]]) -> list[list[float]]:
    """
    The function calculates the inverse of a 2 by 2 matrix. The argument should be of a 2 by 2
    matrix as well
    """
    a, b = lst[0][0], lst[0][1]
    c, d = lst[1][0], lst[1][1]
    determinant = 1/((a * d) - (b * c))
    new_matrix_row1 = [determinant * d, determinant * -b]
    new_matrix_row2 = [determinant * -c, determinant * a]
    return [new_matrix_row1, new_matrix_row2]


def multiply_matrix(lst1: list[list[float]], lst2: list[list[float]]) -> list[list[float]]:
    """
    The function multiplies two matrices where lst1 is the first matrix and lst2 is the second. The
    order MATTERS

    Preconditions:
    - len(lst1[0]) == len(lst2)
    """
    product_matrix = [[0 for _ in range(len(lst2[0]))] for _ in range(len(lst1))]
    for i in range(len(lst1)):
        for j in range(len(lst2[0])):
            for k in range(len(lst2)):
                product_matrix[i][j] += lst1[i][k] * lst2[k][j]

    return product_matrix
