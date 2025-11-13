import numpy as np
from matplotlib import pyplot as plt
import itertools
import matplotlib as mpl

#


class Grid:
    def __init__(self, w, h, cell_size):
        """
        Initialize a grid of width w and height h.
        Each cell has a size of cell_size.
        """
        self.w = w
        self.h = h
        self.cell_size = cell_size
        self.nx = int(w / cell_size)
        self.ny = int(h / cell_size)
        # Create a 2D grid initialized with zeros
        self.grid = np.array([[0 for _ in range(self.nx)] for _ in range(self.ny)])


    def __repr__(self):
        """Display the grid in a readable way."""
        return "\n".join(" ".join(str(c) for c in row) for row in self.grid)

    def clone(self):
        clone = Grid(self.w, self.h, self.cell_size)
        clone.grid = self.grid.copy()
        return clone

    def cell(self, x:int, y:int):
        """
        Get the value of the cell at (x, y).
        (0 <= x < nx, 0 <= y < ny)
        """
        if 0 <= x < self.nx and 0 <= y < self.ny:
            return self.grid[y][x]
        else:
            raise IndexError("Cell coordinates out of range")


    def fill_cell(self, x:int, y:int, value=1):
        """
        Set the cell at (x, y) to 'value'.
        (0 <= x < nx, 0 <= y < ny)
        """
        if 0 <= x < self.nx and 0 <= y < self.ny:
            self.grid[y][x] = value
        else:
            raise IndexError("Cell coordinates out of range")


    def fill_cells(self, a, b, value=1):
        """
        Fill cells in the rectangular area between two points a and b.
        a and b are tuples (x1, y1) and (x2, y2), inclusive.
        """
        x1, y1 = a
        x2, y2 = b

        # Ensure proper ordering
        x_start, x_end = sorted((x1, x2))
        y_start, y_end = sorted((y1, y2))

        for y in range(y_start, y_end + 1):
            for x in range(x_start, x_end + 1):
                self.fill_cell(x, y, value)

    def is_valid(self, x:int, y:int, shape:np.ndarray):
        '''
        input: shape: np.ndarray(positions (x,y))
        Check if the shape fits in the grid at (x, y).
        '''
        for cell in shape+np.array([x,y]):
            nx, ny = cell
            if not 0 <= nx < self.nx or not 0 <= ny < self.ny or not self.cell(nx, ny):
                return False
        return True


    def get_adjacent(self, x:int, y:int):
        """
        Return a list of adjacent cell values (8 directions)
        around the cell at (x, y).
        """
        if not (0 <= x < self.nx and 0 <= y < self.ny):
            raise IndexError("Cell coordinates out of range")
        
        adjacent = []
        mask = np.array([
            [-1,-1], [-1,0], [-1,1],
            [0,-1],          [0,1],
            [1,-1], [1,0],  [1,1]
        ])
        for cell in mask+np.array([x,y]):
            nx, ny = cell
            if 0 <= nx < self.nx and 0 <= ny < self.ny and self.cell(nx, ny):
                adjacent.append([nx, ny])

        return adjacent

    def get_adjacent_count(self, x:int, y:int):
        """
        Return the number of adjacent cells (8 directions)
        that are set to 1 around the cell at (x, y).
        """
        return len(self.get_adjacent(x,y))
    
    def get_direct_adjacent(self, x:int, y:int):
        """
        Return a list of directly adjacent cell values (4 directions)
        around the cell at (x, y).
        """
        if not (0 <= x < self.nx and 0 <= y < self.ny):
            raise IndexError("Cell coordinates out of range")

        adjacent = []
        mask = np.array([
                  [-1,0],
            [0,-1],     [0,1],
                  [1,0],
        ])
        for cell in mask+np.array([x,y]):
            nx, ny = cell
            if 0 <= nx < self.nx and 0 <= ny < self.ny and self.cell(nx, ny):
                adjacent.append([nx, ny])
        return adjacent

    def get_direct_adjacent_count(self, x:int, y:int):
        """
        Return the number of adjacent cells (4 directions)
        that are set to 1 around the cell at (x, y).
        """
        return len(self.get_direct_adjacent(x,y))


    def fuse_with(self, other_grid):
        """
        Fuse this grid with another grid of the same size.
        The resulting grid will have cells set to 1 if either grid has it set to 1.
        """
        if self.nx != other_grid.nx or self.ny != other_grid.ny:
            raise ValueError("Grid sizes do not match for fusion")

        self.grid = np.array(self.grid) + np.array(other_grid.grid)

    
    def __patches(self, p, parents):
        adjacents = self.get_adjacent(p[0], p[1])
        if all(adj in parents for adj in adjacents):
            return parents
        
        parents += adjacents

        adj_patches = []
        for adj in adjacents:
            adj_patches += self.__patches(adj, parents)

        return adj_patches

    def get_patches(self):
        """
        Get a list of all filled patches in the grid.
        Each patch is represented as a list of points (x, y).
        """
        patches = []
        all_patches = []
        for x in range(self.nx):
            for y in range(self.ny):
                if self.cell(x,y):
                    if not [x,y] in all_patches:
                        # print("Exploring patch at:", [x,y])
                        # print("All patches so far:", all_patches)
                        patche = self.__patches([x,y], [[x,y]])
                        patche.sort()
                        patche = list(i for i,_ in itertools.groupby(patche)) # remove duplicates
                        all_patches += patche
                        patches.append(patche)
                        # print("Patch found:", patche)
        return patches


    def inverse(self):
        """
        Inverse the grid: cells with 1 become 0 and cells with 0 become 1.
        """
        self.grid = 1 - np.array(self.grid)
    

    def show(self):
        """Visualize the grid using matplotlib."""
        plt.imshow(self.grid, vmin=0, vmax=self.grid.max(), cmap=mpl.colormaps['tab20'], )
        # plt.xticks(np.arange(-0.5, self.grid.shape[1], 1), [])
        # plt.yticks(np.arange(-0.5, self.grid.shape[0], 1), [])
        # plt.grid(True, which='both', color='black', linestyle='-', linewidth=0.5)
        plt.colorbar()  
        plt.show()


#


if __name__ == "__main__":
    g = Grid(15, 10, 2)
    g.fill_cell(2, 2, 1)
    g.fill_cell(3, 2, 1)
    g.fill_cell(2, 3, 1)
    g.fill_cell(2, 4, 1)

    print(g)
    print(g.grid)
    print("Adjacent to (2,2):", g.get_adjacent_count(2, 2))
    print("Adjacent to (3,3):", g.get_adjacent_count(3, 3))
    print("Direct adjacent to (3,3):", g.get_direct_adjacent_count(3, 3))
    g.show()


    patches = g.get_patches()

    i = 2
    for patch in patches:
        for p in patch:
            g.fill_cell(p[0], p[1], i+g.cell(p[0], p[1]))
        i +=1
    print("Number of patches:", len(patches))
    g.show()