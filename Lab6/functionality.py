import numpy as np


def check_is_optimal(vector_delta_x):
    for i in range(len(vector_delta_x)):
        if vector_delta_x[i] < 0:
            return False, i + 1
    return True, -1


def get_basis_vector(vector, vector_basis):
    vector_res = []
    for i in vector_basis:
        vector_res.append(vector[i-1])

    return vector_res


def get_basis_matrix(matrix, vector_basis):
    matrix_res = np.zeros((len(vector_basis), len(vector_basis)))
    for i in vector_basis:
        for j in vector_basis:
            matrix_res[i-1][j-1] = matrix[i-1][j-1]

    return matrix_res


def create_matrix_h(matrix_d, matrix_a, vector_j_basis_expanded):
    matrix_h = np.zeros((len(vector_j_basis_expanded) + len(matrix_a), len(vector_j_basis_expanded) + len(matrix_a)))
    i_index = 1
    for i in vector_j_basis_expanded:
        j_index = 1
        for j in vector_j_basis_expanded:
            matrix_h[i_index-1][j_index-1] = matrix_d[i-1][j-1]
            if i-1 < len(matrix_a) and j-1 < len(matrix_a[0]):
                matrix_h[i_index - 1 + len(vector_j_basis_expanded)][j_index - 1] = matrix_a[i - 1][j - 1]
                matrix_h[j_index - 1][i_index - 1 + len(vector_j_basis_expanded)] = matrix_a[i - 1][j - 1]
            j_index += 1
        i_index += 1
    # print(matrix_h)
    return matrix_h


def create_l_vector(j_0, vector_j_basis_expanded, vector_x, matrix_d, matrix_a):
    vector_l_res = [0] * len(vector_x)
    vector_l_res[j_0-1] = 1

    matrix_h = create_matrix_h(matrix_d, matrix_a, vector_j_basis_expanded)
    matrix_h_inv = np.linalg.inv(matrix_h)
    vector_b_additional = []

    for i in vector_j_basis_expanded:
        vector_b_additional.append(matrix_d[j_0-1][i-1])

    for i in range(len(matrix_a)):
        vector_b_additional.append(matrix_a[i][j_0-1])

    vector_x_additional = - np.array(matrix_h_inv).dot(np.array(vector_b_additional))

    for i in range(0, j_0-1):
        vector_l_res[i] = vector_x_additional[i]

    return vector_l_res


def get_j_additional(j_0, vector_j_base_expanded, matrix_d, l_basis_expanded, vector_delta_x, vector_x):
    tetta_arr = [np.Infinity] * max(j_0, len(vector_j_base_expanded))

    sigma = np.array(matrix_d).dot(np.array(l_basis_expanded))
    sigma = sigma.dot(np.array(l_basis_expanded))
    if sigma == 0:
        tetta_arr[j_0 - 1] = np.Infinity
    else:
        # print(vector_delta_x[j_0 - 1], sigma)
        tetta_arr[j_0 - 1] = np.abs(vector_delta_x[j_0 - 1]) / sigma

    # print(j_0, tetta_arr)

    for j in vector_j_base_expanded:
        if l_basis_expanded[j - 1] >= 0 and j_0 != j:
            tetta_arr[j - 1] = np.Infinity
        elif j_0 != j:
            tetta_arr[j - 1] = -vector_x[j - 1] / l_basis_expanded[j - 1]
    # print(tetta_arr)
    tetta_0 = min(tetta_arr)

    if tetta_0 == np.Infinity:
        # print("Target task function is not limited by the set of possible options")
        exit(-1)
    j_additional = tetta_arr.index(tetta_0) + 1

    return j_additional, tetta_0


def solve(vector_c, vector_x,
          matrix_a, matrix_d,
          vector_j_base, vector_j_base_expanded):
    vector_c_x = np.array(vector_c) + np.array(matrix_d).dot(np.array(vector_x))
    vector_c_x_basis = get_basis_vector(vector_c_x, vector_j_base)
    matrix_a_basis = get_basis_matrix(matrix_a, vector_j_base)
    matrix_a_basis_inv = np.linalg.inv(matrix_a_basis)

    vector_u_x = - np.array(vector_c_x_basis).dot(np.array(matrix_a_basis_inv))
    vector_delta_x = np.array(vector_u_x).dot(np.array(matrix_a)) + vector_c_x

    is_optimal, j_0 = check_is_optimal(vector_delta_x)
    # print("Vector delta: ", vector_delta_x)
    if is_optimal:
        print("Plan is optimal", vector_x)
        return vector_x

    # print("Index: ", j_0)
    # print(vector_j_base_expanded)
    l_basis_expanded = create_l_vector(j_0, vector_j_base_expanded, vector_x, matrix_d, matrix_a)
    # print(l_basis_expanded)

    j_additional, tetta_0 = get_j_additional(j_0, vector_j_base_expanded,
                                             matrix_d, l_basis_expanded,
                                             vector_delta_x, vector_x)
    # print(j_additional)

    vector_x = vector_x + np.array(l_basis_expanded) * tetta_0
    # print(vector_x)

    if j_0 == j_additional:
        # print("FIRST")
        vector_j_base_expanded.append(j_additional)
    elif j_additional in vector_j_base_expanded and j_additional not in vector_j_base:
        # print("SECOND")
        vector_j_base_expanded.remove(j_additional)
    else:
        s_index = vector_j_base.index(j_additional)
        is_third = False
        # print("THIRD")
        # print(vector_j_base)
        # print(vector_j_base_expanded)
        for i in vector_j_base_expanded:
            if i not in vector_j_base and np.array(matrix_a_basis).dot(np.array(matrix_a[:, i-1]))[s_index] != 0:
                vector_j_base[j_additional] = i
                vector_j_base_expanded.remove(j_additional)
                is_third = True
                break
        if not is_third:
            vector_j_base[vector_j_base.index(j_additional)] = j_0
            vector_j_base_expanded[vector_j_base_expanded.index(j_additional)] = j_0

    return solve(vector_c, vector_x, matrix_a, matrix_d, vector_j_base, vector_j_base_expanded)
