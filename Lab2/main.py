import numpy as np


def multiply_matrix_on_vector(inverse_matrix, vector):
    result_matrix = []

    for j in range(len(inverse_matrix)):
        sum_of_row = 0
        for i in range(len(inverse_matrix)):
            sum_of_row += inverse_matrix[j][i] * vector[i]

        result_matrix.append(sum_of_row)

    return result_matrix


def multiply_vector_on_matrix(vector, matrix):
    result_vector = []
    for i in range(len(matrix[0])):
        sum_of_col = 0

        for j in range(len(vector)):
            sum_of_col += matrix[j][i]*vector[j]

        result_vector.append(sum_of_col)

    return result_vector


def multiply_vector_on_digit(vector, digit):
    for i in range(len(vector)):
        vector[i] *= (-1 / digit)


def create_q_matrix(vector, index):
    identity_matrix = []

    for i in range(len(vector)):
        row = []

        for j in range(len(vector)):
            if j == index:
                row.append(vector[i])
            elif i == j:
                row.append(1)
            else:
                row.append(0)

        identity_matrix.append(row)

    return identity_matrix


def multiply_matrix_on_q_matrix(inverse_matrix, q_matrix, index):
    result_matrix = []

    for i in range(len(inverse_matrix)):
        row = []
        for j in range(len(inverse_matrix)):
            if i != index:
                row.append(inverse_matrix[i][j] * q_matrix[i][i] + inverse_matrix[index][j] * q_matrix[i][index])
            else:
                row.append(inverse_matrix[index][j] * q_matrix[i][index])

        result_matrix.append(row)

    return result_matrix


def calculate_inverse_matrix(matrix, inverse_matrix, x_vector, i):
    result_vector = multiply_matrix_on_vector(inverse_matrix, x_vector)

    print(inverse_matrix, x_vector)

    if result_vector[i - 1] == 0:
        raise Exception("Matrix is irreversible")

    vector = result_vector.copy()
    vector[i - 1] = -1

    multiply_vector_on_digit(vector, result_vector[i - 1])

    q_matrix = create_q_matrix(vector, i - 1)

    return multiply_matrix_on_q_matrix(inverse_matrix, q_matrix, i - 1)


def get_base_matrix(a_matrix, b_basis_plan):
    a_base_matrix = []

    for j in range(len(b_basis_plan)):
        arr = []
        for i in b_basis_plan:
            arr.append(a_matrix[j][i - 1])
        a_base_matrix.append(arr)

    return a_base_matrix


def get_inverse_matrix(a_matrix, b_basis_plan):
    a_base_matrix = get_base_matrix(a_matrix, b_basis_plan)

    return a_base_matrix, np.linalg.inv(a_base_matrix)


def main_phase_of_simplex_method(c_vector, a_matrix, a_base_matrix, inverse_matrix, x_basis_plan, b_basis_plan, b_basis_result):
    print(a_matrix, inverse_matrix)
    c_vector_base = []
    for i in b_basis_plan:
        c_vector_base.append(c_vector[i-1])

    print("Vector_base ", c_vector_base)
    potential_vector = multiply_vector_on_matrix(c_vector_base, inverse_matrix)
    print("Potential vector ", potential_vector)

    mark_vector = []
    help_vector = multiply_vector_on_matrix(potential_vector, a_matrix)
    print("Help vector ", help_vector)
    for i in range(len(help_vector)):
        mark_vector.append(help_vector[i] - c_vector[i])
    print("Mark vector ", mark_vector)
    j = check_is_optimal(mark_vector)
    print("J", j)
    if j == len(mark_vector):
        print("Plan is optimal", x_basis_plan)
        return

    a_j = []
    for i in range(len(a_matrix)):
        a_j.append(a_matrix[i][j-1])

    z_vector = multiply_matrix_on_vector(inverse_matrix, a_j)
    print(z_vector)

    q_vector = []

    for i in range(len(z_vector)):
        if z_vector[i] <= 0:
            q_vector.append(np.Infinity)
        else:
            print(b_basis_result[i], x_basis_plan)
            q_vector.append(x_basis_plan[b_basis_result[i]-1] / z_vector[i])

    print("Q_vector: ", q_vector)
    q_0 = min(q_vector)

    if q_0 == np.Infinity:
        Exception("The objective functional of the problem is not bounded from above on the set of admissible plans")

    k = q_vector.index(q_0)
    j_k = b_basis_plan[k]
    print("K: ", k)
    print("J_k: ", j_k)

    b_basis_result[k] = j
    print(b_basis_plan)

    print("X_basis_plan ", x_basis_plan)

    for i in range(len(b_basis_plan)):
        if i != k:
            x_basis_plan[b_basis_result[i]-1] = (x_basis_plan[b_basis_result[i]-1] - q_0*z_vector[i])

    x_basis_plan[j_k - 1] = 0
    x_basis_plan[j - 1] = q_0
    print(x_basis_plan)
    a_new_base_matrix = get_base_matrix(a_matrix, b_basis_result)

    inverse_new_matrix = calculate_inverse_matrix(a_base_matrix, inverse_matrix, np.array(a_matrix)[:, j-1], k+1)

    main_phase_of_simplex_method(c_vector, a_matrix, a_new_base_matrix, inverse_new_matrix, x_basis_plan, b_basis_plan, b_basis_result)

    return


def check_is_optimal(mark_vector):
    for i in range(len(mark_vector)):
        if mark_vector[i] < 0:
            return i + 1

    return len(mark_vector)


def lab2_test():
    c_vector_example = [1, 1, 0, 0, 0]
    a_matrix_example = [[-1, 1, 1, 0, 0],
                        [1, 0, 0, 1, 0],
                        [0, 1, 0, 0, 1]]
    x_vector_base = [0, 0, 1, 3, 2]
    b_indexes_base = [3, 4, 5]
    b_indexes_base_result = b_indexes_base
    a_base_matrix, inverse_matrix = get_inverse_matrix(a_matrix_example, b_indexes_base)
    main_phase_of_simplex_method(c_vector_example, a_matrix_example, a_base_matrix,
                                 inverse_matrix, x_vector_base, b_indexes_base, b_indexes_base_result)


def lab1_test():
    matrix_example = [[1, 0, 5],
                      [2, 1, 6],
                      [3, 4, 0]]
    inverse_matrix_example = [[-24, 20, -5],
                              [18, -15, 4],
                              [5, -4, 1]]
    x_vector_example = [2, 2, 2]
    i = 2
    print(np.linalg.inv([[1, 2, 5],
                      [2, 2, 6],
                      [3, 2, 0]]))
    print(calculate_inverse_matrix(matrix_example,
                                   inverse_matrix_example,
                                   x_vector_example, i))
    matrix_example2 = [[2, 5, 7],
                       [6, 3, 4],
                       [5, -2, -3]]
    inverse_matrix_example2 = [[1, -1, 1],
                               [-38, 41, -34],
                               [27, -29, 24]]
    x_vector_example2 = [2, 1, 3]
    i2 = 1
    print(calculate_inverse_matrix(matrix_example2,
                                   inverse_matrix_example2,
                                   x_vector_example2, i2))

    matrix_example3 = [[1,-1,3,2,4],
                       [2,-3,2,-2,-6],
                       [3,-5,1,4,2],
                       [4,-2,-1,-3,-1],
                       [5,-1,0,1,2]]
    inverse_matrix_example3 = [[-21/650, 4/75, -113/1950, -47/975, 84/325],
                                [-11/325, 1/25, -61/325, -68/325, 88/325],
                                [161/650, 11/75, -217/1950, -73/975, 6/325],
                                [-97/650, 1/25, 53/650, -93/325, 63/325],
                                [9/65, -2/15, 2/195, 31/195, -7/65]]
    x_vector_example3 = [2, 1, 3,-1,2]
    i3 = 4
    print(calculate_inverse_matrix(matrix_example3,
                                   inverse_matrix_example3,
                                   x_vector_example3, i3))


if __name__ == '__main__':
    lab2_test()
