from functionality import solve


if __name__ == '__main__':
    vector_c_example = [-8, -6, -4, -6]
    matrix_d_example = [[2, 1, 1, 0],
                        [1, 1, 0, 0],
                        [1, 0, 1, 0],
                        [0, 0, 0, 0]]
    matrix_a_example = [[1, 0, 2, 1],
                        [0, 1, -1, 2]]
    j_base_example = [1, 2]
    j_base_expanded_example = [1, 2]
    vector_x_example = [2, 3, 0, 0]
    solve(vector_c_example, vector_x_example,
          matrix_a_example, matrix_d_example,
          j_base_example, j_base_expanded_example)
