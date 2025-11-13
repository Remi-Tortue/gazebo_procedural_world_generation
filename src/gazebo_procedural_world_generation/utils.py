import numpy as np
import math
import yaml
import pathlib

#


def get_package_path():
    pkg_path = pathlib.Path(__file__).parent.resolve()
    return str(pkg_path)

def get_project_path():
    pkg_path = pathlib.Path(__file__).parent.parent.parent.resolve()
    return str(pkg_path)

def load_config(config_file):
    pkg_path = get_project_path()
    config_path = pkg_path + "/config/" + config_file + ".yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)


    return config


def footprint_to_obstacle_grid_shape(footprint, scale, cell_size):
    real_footprint = np.array(footprint) * scale
    cell_footprint = real_footprint / cell_size
    grid_shape = []
    min_x = math.ceil(min(0, cell_footprint[0]))
    max_x = math.ceil(max(0, cell_footprint[0]))
    if not max_x:
        max_x +=1
    min_y = math.ceil(min(0, cell_footprint[1]))
    max_y = math.ceil(max(0, cell_footprint[1]))
    if not max_y:
        max_y +=1
    # print(min_x, max_x, min_y, max_y)
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            grid_shape.append([x, y])
    return np.array(grid_shape)


def load_grid_obstacles(config, cell_size):
    pkg_path = get_package_path()
    
    obstacles = config["objects"]
    S = {}
    for key in obstacles.keys():
        

        if 'grid_shape' in obstacles[key]:
            grid_shape = np.array(obstacles[key]['grid_shape'])
        else:
            obstacle_config_path = pkg_path + obstacles[key]['obstacle_config_path']
            with open(obstacle_config_path, 'r') as f:
                obstacle_config = yaml.safe_load(f)
            footprint = obstacle_config['obstacle']['footprint']
            scale = obstacle_config['obstacle']['scale']
            grid_shape = footprint_to_obstacle_grid_shape(footprint, scale, cell_size)
        S[key] = grid_shape
    return S






if __name__ == "__main__":
    from gazebo_procedural_world_generation import Grid
    w = 10
    h = 10
    cell_size = 1.
    grid = Grid(w, h, cell_size)

    footprint = [1.2,0.8]
    scale = 1.0
    grid_shape = footprint_to_obstacle_grid_shape(footprint, scale, cell_size)
    print(grid_shape)


    shape_pose = [2, 3]
    for cell in grid_shape:
        x, y = cell + np.array(shape_pose)
        grid.fill_cell(x, y)
    grid.show()

    print(get_package_path())
    print(get_project_path())
    print(load_config('world_params'))