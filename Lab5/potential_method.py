import numpy as np
import copy


def check_has_solution(vector_a, vector_b):
    return sum(vector_a) == sum(vector_b)


def fill_matrix_x(vector_a, vector_b, matrix_x):
    i = 0
    j = 0

    vector_basis_index = []

    while i != len(vector_a) and j != len(vector_b):
        if max(vector_a[i], vector_b[j]) == vector_a[i] and i > j:
            vector_a[i] -= vector_b[j]
            matrix_x[i][j] = vector_b[j]
            vector_basis_index.append((i, j))
            j += 1
        elif max(vector_a[i], vector_b[j]) == vector_b[j] and j <= i:
            vector_b[j] -= vector_a[i]
            matrix_x[i][j] = vector_a[i]
            vector_basis_index.append((i, j))
            i += 1

    return vector_basis_index


def check_is_optimal(vector_basis_index, vector_res, matrix_c, m, n):
    for i in range(m):
        for j in range(n):
            if not vector_basis_index.__contains__((i, j)):
                if matrix_c[i][j] < (vector_res[i]+vector_res[j+m]):
                    return False, (i, j)

    return True, (0, 0)


def solve(vector_a, vector_b, matrix_c):
    m = len(vector_a)
    n = len(vector_b)

    if not check_has_solution(vector_a, vector_b):
        raise Exception("Balance condition isn't met")

    matrix_x = np.zeros((m, n))
    vector_basis_index = fill_matrix_x(vector_a, vector_b, matrix_x)

    while True:
        matrix_u_v = []
        vector_u_v_res = []

        for i, j in vector_basis_index:
            arr = [0] * (m + n)
            arr[i] = 1
            arr[j + m] = 1
            matrix_u_v.append(arr)
            vector_u_v_res.append(matrix_c[i][j])

        index = matrix_u_v[0].index(1)
        for i in range(len(matrix_u_v)):
            _ = matrix_u_v[i].pop(index)

        vector_res = np.linalg.solve(np.array(matrix_u_v), np.array(vector_u_v_res))

        vector_res = list(vector_res)
        vector_res.insert(index, 0.0)
        # print(vector_res)

        check, index = check_is_optimal(vector_basis_index, vector_res, matrix_c, m, n)
        # print("CHANGE ", index)
        if check:
            print("Plan is optimal")
            print(matrix_x)
            return

        i_prev = vector_basis_index[0][0]
        j_prev = vector_basis_index[0][1]

        position = 0
        for i, j in vector_basis_index[1:]:
            position += 1
            if i_prev == i:
                i_prev = i
                j_prev = j
                continue
            if j_prev == j:
                i_prev = i
                j_prev = j
                continue
            vector_basis_index.insert(position, index)
            break
        if position == len(vector_basis_index)-1:
            vector_basis_index.append(index)

        # print("vector_basis ", vector_basis_index)
        vector_basis_index_copy = copy.deepcopy(vector_basis_index)

        for i in range(len(matrix_x)):
            sum_index = 0
            copy_i_index = 0
            copy_j_index = 0
            for i_index, j_index in vector_basis_index_copy:
                if i_index == i:
                    sum_index += 1
                    copy_i_index = i_index
                    copy_j_index = j_index
            if sum_index == 1:
                vector_basis_index_copy.remove((copy_i_index, copy_j_index))

        for j in range(len(matrix_x[0])):
            sum_index = 0
            copy_i_index = 0
            copy_j_index = 0
            for i_index, j_index in vector_basis_index_copy:
                if j_index == j:
                    sum_index += 1
                    copy_i_index = i_index
                    copy_j_index = j_index
            if sum_index == 1:
                vector_basis_index_copy.remove((copy_i_index, copy_j_index))
        # print("BASIS: ", vector_basis_index)
        # print("BASIS COPY: ", vector_basis_index_copy)

        vector_calc = [0]*len(vector_basis_index_copy)
        plus = True
        begin_index = vector_basis_index_copy.index(index)
        # print("INDEX:", begin_index)
        begin_index_copy = begin_index - 1
        while begin_index < len(vector_basis_index_copy):
            i = vector_basis_index_copy[begin_index][0]
            j = vector_basis_index_copy[begin_index][1]
            if vector_basis_index_copy.__contains__((i, j)):
                vector_calc[begin_index] = (plus, matrix_x[i][j])
                plus = not plus
            begin_index += 1

        plus = False
        while begin_index_copy >= 0:
            i = vector_basis_index_copy[begin_index_copy][0]
            j = vector_basis_index_copy[begin_index_copy][1]
            if vector_basis_index_copy.__contains__((i, j)):
                vector_calc[begin_index_copy] = (plus, matrix_x[i][j])
                plus = not plus
            begin_index_copy -= 1

        # print(vector_calc)
        min_value = min(j for i, j in vector_calc if not i)
        # print(min_value)
        index_old = []
        # print(matrix_x)
        counter = 0
        for i, j in vector_basis_index_copy:
            if vector_basis_index_copy.__contains__((i, j)):
                if vector_calc[counter][0]:
                    matrix_x[i][j] += min_value
                else:
                    matrix_x[i][j] -= min_value
                if matrix_x[i][j] == 0:
                    index_old.append((i, j))

            counter += 1
        index_old = sorted(index_old)
        vector_basis_index.remove(index_old[0])
