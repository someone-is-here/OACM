def multiply_matrix_on_vector(inverse_matrix, vector):
    result_matrix = []

    for i in range(len(inverse_matrix)):
        sum_of_row = 0

        for j in range(len(inverse_matrix)):
            sum_of_row += inverse_matrix[i][j] * vector[j]

        result_matrix.append(sum_of_row)

    return result_matrix


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

    if result_vector[i - 1] == 0:
        raise Exception("Matrix is irreversible")

    vector = result_vector.copy()
    vector[i - 1] = -1

    multiply_vector_on_digit(vector, result_vector[i - 1])

    q_matrix = create_q_matrix(vector, i - 1)

    return multiply_matrix_on_q_matrix(inverse_matrix, q_matrix, i - 1)


def lab1_test():
    matrix_example = [[1, 0, 5],
                      [2, 1, 6],
                      [3, 4, 0]]
    inverse_matrix_example = [[-24, 20, -5],
                              [18, -15, 4],
                              [5, -4, 1]]
    x_vector_example = [2, 2, 2]
    i = 2
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
    lab1_test()
