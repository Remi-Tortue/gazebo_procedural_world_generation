import random
from gazebo_procedural_world_generation import Grid


#


def workspace_partitioning(X:Grid, seed, crouding_factor = 0.4) -> Grid:
    random.seed(seed)
    grid = X.clone()

    crouding_factor = 1 - crouding_factor
    clustering_factor = 0.8
    clustering_factor = 1 - clustering_factor
    
    for i in range(grid.nx):
        for j in range(grid.ny):
            if random.random() < crouding_factor:
                grid.fill_cell(i,j)

    grid_clustering = X.clone()
    for i in range(grid.nx):
        for j in range(grid.ny):
            if not grid.cell(i,j):
                nb_adj = grid.get_adjacent_count(i, j)
                if random.random() < clustering_factor * nb_adj:
                    grid_clustering.fill_cell(i,j)
    grid.fuse_with(grid_clustering)

    grid.inverse()

    output = X.clone()
    output.fuse_with(grid)
    return output


#


def perlin_noise(X:Grid, seed, scale=5.0, threshold=0.2) -> Grid:
    try:
        from noise import pnoise2
    except ImportError:
        raise ImportError("The 'noise' library is required for Perlin noise generation. Please install it via 'pip install noise'.")

    grid = X.clone()

    for i in range(grid.nx):
        for j in range(grid.ny):
            x = i / grid.nx * scale
            y = j / grid.ny * scale
            noise_value = pnoise2(x, y, base=seed)
            if noise_value > threshold:
                grid.fill_cell(i,j)

    output = X.clone()
    output.fuse_with(grid)
    return output