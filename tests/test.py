import pytest
import numpy as np
from gazebo_procedural_world_generation import utils, Grid


#


@pytest.fixture
def default_grid():
    return Grid(10, 10, 1.0)

@pytest.mark.parametrize("footprint, expected_grid_shape", [
    ([1.2, 1.0], [[0., 0.], [1., 0.]]),
    ([2., 1.0], [[0., 0.], [1., 0.]]),
    ([2., 1.1], [[0., 0.], [0., 1.],[1., 0.], [1., 1.]]),
])


#


def test_footprint_to_obstacle_grid_shape(default_grid, footprint, expected_grid_shape):

    grid_shape = utils.footprint_to_obstacle_grid_shape(footprint, default_grid.cell_size)

    np.testing.assert_array_equal(grid_shape, expected_grid_shape)


def test_fill_cell(default_grid):

    default_grid.fill_cell(0, 0)

    assert default_grid.cell(0, 0) == 1
    assert default_grid.cell(1, 0) == 0
