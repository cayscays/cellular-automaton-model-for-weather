#
# Author:       cayscays
# Date:         November 2021
# Version:      1
# Class world: an implantation of the cellular automaton on a grid.
#

from model.rules import *


class World:
    # no parameters --> random
    # file          --> from file
    # other         --> deep copy of other World
    # question      --> pre-defined World for questions 2c,2d
    def __init__(self, other, random_layout, question):
        self.grid = []
        self.day = 0
        # Random layout:
        if random_layout:
            for i in range(GRID_HEIGHT):
                col = []
                for j in range(GRID_WIDTH):
                    # random initiation:
                    col.append(cell_from_random_with_init_rules())
                self.grid.append(col)
        # pre-defined World for questions 2c,2d
        elif other is None:
            if question == '2c':
                for i in range(GRID_HEIGHT):
                    col = []
                    for j in range(GRID_WIDTH):
                        # random initiation:
                        col.append(cell_from_landscape_with_init_rules(pre_defined_world_map[i][j]))
                    self.grid.append(col)
            elif question == '2d':
                j = 0
                for i in range(GRID_HEIGHT):
                    col = []
                    for k in range(GRID_WIDTH):
                        # random initiation:
                        col.append(Cell(d_wind_speed[j], d_wind_direction[j], d_temp[j], d_pollution[j], d_clouds[j],
                                        d_height[j], d_landscapes[j], d_rain[j]))
                        j += 1
                    self.grid.append(col)
        # Deep copy
        else:
            for i in range(GRID_HEIGHT):
                col = []
                for j in range(GRID_WIDTH):
                    col.append(other.grid[i][j].deep_copy())
                self.grid.append(col)

    # --> Deep copy of the World
    def deep_copy(self):
        return World(other=self, random_layout=False, question=None)

    # Update the world's state for the next generation
    # Saves the prev generation state using deep copy
    def update(self, stats_file):
        prev_generation = World(other=self, random_layout=False, question=None)
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                nw = prev_generation.grid[(i - 1) % GRID_HEIGHT][(j - 1) % GRID_WIDTH]
                n = prev_generation.grid[(i - 1) % GRID_HEIGHT][j]
                ne = prev_generation.grid[(i - 1) % GRID_HEIGHT][(j + 1) % GRID_WIDTH]
                e = prev_generation.grid[i % GRID_HEIGHT][(j + 1) % GRID_WIDTH]
                w = prev_generation.grid[i % GRID_HEIGHT][(j - 1) % GRID_WIDTH]
                s = prev_generation.grid[(i + 1) % GRID_HEIGHT][j]
                sw = prev_generation.grid[(i + 1) % GRID_HEIGHT][(j - 1) % GRID_WIDTH]
                se = prev_generation.grid[(i + 1) % GRID_HEIGHT][(j + 1) % GRID_WIDTH]
                self.grid[i][j].update(nw=nw, n=n, ne=ne, w=w, e=e, s=s, se=se, sw=sw)
                stats_file.update_raw(self.day, self.grid[i][j].get_state())
        self.day += 1


# Random layout following init rules
world = World(other=None, random_layout=True, question=None)
