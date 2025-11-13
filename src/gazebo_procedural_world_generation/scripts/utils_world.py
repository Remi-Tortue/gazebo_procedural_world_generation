from matplotlib import pyplot as plt


#


class World:
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
