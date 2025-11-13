import numpy as np
import random
import math
import yaml
import matplotlib.pyplot as plt
import importlib.util
import time

from gazebo_procedural_world_generation import filling, tiling, utils
from gazebo_procedural_world_generation import Grid, World

#


if __name__ == "__main__":
    config_file = 'world_params'

    config = utils.load_config(config_file)
    w = config["world"]["width"]
    h = config["world"]["height"]
    cell_size = config["world"]["cell_size"]
    seed = config["world"]["seed"]

    grid = Grid(w, h, cell_size)

    grid = filling.perlin_noise(grid, seed)
    # grid = filling.workspace_partitioning(grid, seed)

    patches = grid.get_patches()

    # get the list of obstacle shapes from config
    S = utils.load_grid_obstacles(config, cell_size)
    print(f'S: {S}')

    color_grid = grid.clone() # for grid ploting
    patches_tiling_solutions = []
    for patch in patches:
        tiling_solutions = tiling.dance_steps_tiling_patch(grid, patch, S, single_solution=True, seed = 0)
        patches_tiling_solutions.append(tiling_solutions)

        i = 1
        for shape in tiling_solutions[0]:
            for cell in (S[shape['name']]+np.array(shape['position'])).tolist():
                color_grid.fill_cell(cell[0], cell[1], i)
            i += 1
    color_grid.show()

    world = World(config)
    print(world)

    # add grid obstacles to the world
    for patch in range(len(patches_tiling_solutions)):
        patche_tiling_solution = patches_tiling_solutions[patch][0]
        for obstacle in patche_tiling_solution:
            # print(patche_tiling_solution)
            world.add_obstacle(obstacle['name'], obstacle['position'], cell_size)


    # print(world)
    world.save_world()
