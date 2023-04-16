import numpy as np

from functionality import simplex_method, get_inverse_matrix,\
    multiply_vector_on_matrix, check_is_optimal, get_base_matrix,\
    calculate_inverse_matrix, multiply_matrix_on_vector


def create_optimal_plan(vector_c, basis_vector, pseudo_plan_vector):
    k = [0] * len(vector_c)
    j = 0
    for i in basis_vector:
        k[i - 1] = pseudo_plan_vector[j]
        j += 1

    return k


def check_optimal(k):
    for i in range(len(k)-1, -1, -1):
        if k[i] < 0:
            return i + 1

    return -1


def multiply_vector_on_vector(vector_1, vector_2):
    if len(vector_1) != len(vector_2):
        raise Exception("Can't multiply vector on vector. Different vector's length")
    return sum([vector_1[i]*vector_2[i] for i in range(len(vector_1))])


def dual_simplex_method(vector_c, matrix_a, a_base_matrix, inverse_matrix, vector_b, basis_vector):
    print("A base: ", a_base_matrix)
    print("A inverse: ", inverse_matrix)

    vector_c_basis = [vector_c[i-1] for i in basis_vector]
    print("Vector_c: ", vector_c_basis)

    # basic admissible plan of the dual problem
    basis_plan_dual_vector = multiply_vector_on_matrix(vector_c_basis, inverse_matrix)
    print("Basis plan dual vector: ", basis_plan_dual_vector)

    pseudo_plan_vector = multiply_matrix_on_vector(inverse_matrix, vector_b)
    print("Pseudo plan: ", pseudo_plan_vector)

    k = create_optimal_plan(vector_c, basis_vector, pseudo_plan_vector)
    print("k: ", k)
    j_k = check_optimal(k)

    if j_k == -1:
        print("Plan is optimal", k, basis_vector)
        return k

    print("j_k", j_k)
    j_k_index = basis_vector.index(j_k) + 1
    print("j_k_index: ", j_k_index)

    delta_y_vector = inverse_matrix[j_k_index - 1]
    print("delta_y: ", delta_y_vector)

    mu = {}
    for i in range(1, len(vector_c) + 1):
        if i not in basis_vector:
            mu[i-1] = (multiply_vector_on_vector(delta_y_vector,
                                                np.array(matrix_a)[:, i-1]))
    print("Mu: ", mu)

    is_feasible = True
    for i in mu:
        if i < 0:
            is_feasible = False

    if not is_feasible:
        raise Exception("Problem is infeasible")

    sigma = []
    for i in range(1, len(vector_c) + 1):
        if i not in basis_vector and mu[i-1] < 0:
            sigma.append((vector_c[i-1] - multiply_vector_on_vector(basis_plan_dual_vector,
                                                np.array(matrix_a)[:, i-1])) / mu[i - 1])
    print("Sigma: ", sigma)

    sigma_0 = min(sigma)
    j_0 = sigma.index(sigma_0) + 1
    print("Sigma0: ", sigma_0, "\nJ_0: ", j_0)
    basis_vector[j_k_index-1] = j_0
    print("Result basis: ", basis_vector)

    a_new_base_matrix = get_base_matrix(matrix_a, basis_vector)
    inverse_new_matrix = calculate_inverse_matrix(a_base_matrix, inverse_matrix,
                                                  np.array(matrix_a)[:, j_0 - 1], j_k_index)
    print("Inverse: ", inverse_new_matrix)

    return dual_simplex_method(vector_c, matrix_a, a_new_base_matrix, inverse_new_matrix, vector_b, basis_vector)


def lab4_test():
    c_vector_example = [-4, -3, -7, 0, 0]
    a_matrix_example = [[-2, -1, -4, 1, 0],
                        [-2, -2, -2, 0, 1]]
    b_indexes_base = [-1, -1.5]
    b_base = [4, 5]

    a_base_matrix, inverse_matrix = get_inverse_matrix(a_matrix_example, b_base)

    print(dual_simplex_method(c_vector_example, a_matrix_example, a_base_matrix, inverse_matrix,
                              b_indexes_base, b_base))


if __name__ == '__main__':
    lab4_test()
