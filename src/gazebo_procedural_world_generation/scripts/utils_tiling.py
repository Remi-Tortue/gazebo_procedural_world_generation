import numpy as np
import exact_cover as ec
from gazebo_procedural_world_generation import Grid
import random

#


def generate_A_from_filtered_cells(X:Grid, problem_columns:list, S:list, seed = 0):
    A = []
    problem_rows = []
    for s in S:
        for c in problem_columns:
            x, y = c
            if X.is_valid(x,y,s):
                row = np.zeros(len(problem_columns))
                for cell in (s+np.array([x,y])).tolist():
                    row[problem_columns.index(cell)] = 1
                A.append(row)
                problem_rows.append([s, c])
    A = np.array(A, dtype=bool)
    if seed != 0: np.random.default_rng(seed = seed).shuffle(A, axis=0) # to shuffle the type of shapes
    return A, problem_columns, problem_rows


def generate_A(X:Grid, S:list, seed = 0):
    '''
    input:
        X: Grid
        S: List of shapes (numpy arrays)
    Generate the exact cover matrix A for grid X and shapes S.
    '''
    problem_columns = [[x,y] for x in range(X.nx) for y in range(X.ny) if X.cell(x,y)]
    return generate_A_from_filtered_cells(X, problem_columns, S, seed = seed)


#

def extrat_shape_list(shapes_dict:dict):
    shapes = []
    for key in shapes_dict.keys():
        shapes.append(shapes_dict[key])
    return shapes


def dance_steps_tiling_patch(X:Grid, patch:list, shapes_dict:dict, single_solution=False, seed = 0):
    '''
    input:
        X: Grid
        patch: list
        shapes_dict: dict {'name': shape:np.ndarray}
    output:
        tiling_solutions: list of list (solutions) of dict {'position':np.ndarray, 'name':str}
    Generate the exact cover solutions for grid X and shapes S.
    Way faster with single_solution = True for a single soution.
    '''

    shapes = extrat_shape_list(shapes_dict)
    A, problem_columns, problem_rows = generate_A_from_filtered_cells(X, patch, shapes, seed = seed)
    if A == [] or A is None:
        print('exact cover: no solution')
        return [[]]
    
    print('exact cover...')
    if ec.get_solution_count(A) == 1 or single_solution:
        x_algorithms_solutions = [ec.get_exact_cover(A)]
    elif ec.get_solution_count(A) == 0:
        print('exact cover: no solution')
        return [[]]
    else:
        x_algorithms_solutions = ec.get_all_solutions(A)
    print('exact cover done')

    tiling_solutions = []
    for solution in x_algorithms_solutions:
        tiling = []
        for row_index in solution:
            s, c = problem_rows[row_index]
            tile = {}
            tile['position'] = c
            for key, value in shapes_dict.items():
                if np.array_equal(s, value):
                    tile['name'] = key
            tiling.append(tile)
        tiling_solutions.append(tiling)
    return tiling_solutions





#


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    X = Grid(15, 10, 2)
    X.fill_cell(2, 2, 1)
    X.fill_cell(3, 2, 1)
    X.fill_cell(2, 3, 1)
    X.fill_cell(2, 4, 1)
    print(X)


    S = {}
    S['horizontal bar'] = np.array([[0,0],[1,0]])
    S['vertical bar'] = np.array([[0,0],[0,1]])
    S['box'] =  np.array([[0,0]])
    S['big box'] =  np.array([[0,0],[1,0],[0,1],[1,1]])

    shapes_list = extrat_shape_list(S)
    A, problem_columns, problem_rows = generate_A(X, shapes_list)
    print(A)
    plt.imshow(A)
    plt.show()

    patches = X.get_patches()
    tiling_solutions = dance_steps_tiling_patch(X, patches[0], S, single_solution=False)
    print(tiling_solutions)

    for solution in tiling_solutions:
        solution_grid = X.clone()
        i = 1
        for shape in solution:
            for cell in (S[shape['name']]+np.array(shape['position'])).tolist():
                solution_grid.fill_cell(cell[0], cell[1], i)
            i += 1
        solution_grid.show()