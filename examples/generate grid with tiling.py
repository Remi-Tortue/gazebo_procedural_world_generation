import numpy as np
import random
import math
import yaml
import matplotlib.pyplot as plt
import importlib.util
import time

from gazebo_procedural_world_generation import filling, tiling, utils
from gazebo_procedural_world_generation import Grid

#


if __name__ == "__main__":
    config_file = 'world_params'

    config = utils.load_config(config_file)

    seed = config["world"]["seed"]
    # seed=random.randint(0, 100)
    w = config["world"]["width"]
    h = config["world"]["height"]
    cell_size = config["world"]["cell_size"]

    grid = Grid(w, h, cell_size)

    # grid.fill_cells((0,0), (grid.nx-1, 0))
    # grid.fill_cells((0,0), (0, grid.ny-1))
    # grid.fill_cells((grid.nx-1, grid.ny-1), (grid.nx-1, 0))
    # grid.fill_cells((grid.nx-1, grid.ny-1), (0, grid.ny-1))


    grid = filling.perlin_noise(grid, seed)
    # grid = utils_filling.workspace_partitioning(grid, seed)

    patches = grid.get_patches()

    color_grid = grid.clone()
    i = 2
    for patch in patches:
        for p in patch:
            color_grid.fill_cell(p[0], p[1], i+color_grid.cell(p[0], p[1]))
        i +=1
    print("Number of patches:", len(patches))

    color_grid.show()

    S = {}
    S['big box'] =  np.array([[0,0],[1,0],[0,1],[1,1]])
    S['horizontal bar'] = np.array([[0,0],[1,0]])
    S['vertical bar'] = np.array([[0,0],[0,1]])
    S['box'] =  np.array([[0,0]])
    
    patches_tiling_solutions = []
    for patch in patches:
        tiling_solutions = tiling.dance_steps_tiling_patch(grid, patch, S, single_solution=True, seed = 0)
        patches_tiling_solutions.append(tiling_solutions)

        # for solution in tiling_solutions:
        #     color_grid = grid.clone()
        #     i = 1
        #     for shape in solution:
        #         for cell in (S[shape['name']]+np.array(shape['position'])).tolist():
        #             color_grid.fill_cell(cell[0], cell[1], i)
        #         i += 1
        #     color_grid.show()

    color_grid = grid.clone()
    for solutions in patches_tiling_solutions:
        i = 1
        for shape in solutions[0]:
            for cell in (S[shape['name']]+np.array(shape['position'])).tolist():
                color_grid.fill_cell(cell[0], cell[1], i)
            i += 1
    color_grid.show()

    