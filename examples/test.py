import numpy as np
import random
import math
import yaml
import matplotlib.pyplot as plt
import importlib.util
import time

from gazebo_procedural_world_generation import filling_algorithms, utils_tiling
from gazebo_procedural_world_generation import Grid

#


if __name__ == "__main__":
    config_name = 'world_params'

    spec = importlib.util.find_spec("gazebo_procedural_world_generation")
    if spec:
        if spec.submodule_search_locations:
            config_path = spec.submodule_search_locations[0] + "/config/" + config_name + ".yaml"
            print(config_path)
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

    # seed = config["world"]["seed"]
    seed=random.randint(0, 100)
    # seed = 1
    w = config["world"]["width"]
    h = config["world"]["height"]
    cell = config["world"]["cell_size"]

    grid = Grid(w, h, cell)

    grid.fuse_with(filling_algorithms.perlin_noise(w ,h, cell, seed))

    patches = grid.get_patches()

    S =