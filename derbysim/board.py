
from . import Cube

class Board:
    size = 46

    def __init__(self):
        self.spaces = list()
        for _ in range(self.size + 1):
            self.spaces.append(list())
        self.first_half_complete = False

    def get_below(self, cube: Cube):
        assert cube in self.spaces[cube.pos]
        rv = list()
        for stacked_cube in self.spaces[cube.pos]:
            if id(stacked_cube) == id(cube):
                break
            else:
                rv.append(stacked_cube)
        return rv
    
    def get_above(self, cube: Cube):
        assert cube in self.spaces[cube.pos]
        rv = list()
        found = False
        for stacked_cube in self.spaces[cube.pos]:
            if id(stacked_cube) == id(cube):
                found = True
                continue
            if found:
                rv.append(stacked_cube)
        return rv

    def move_cube(self, cube: Cube) -> bool:
        rv = False
        assert cube in self.spaces[cube.pos]
        # remove cube from current space
        self.spaces[cube.pos].remove(cube)
        # increment cubes' position
        cube.pos += 1
        # check if the race is over
        if not self.first_half_complete and cube.pos >= (self.size / 2):
            self.first_half_complete = True
            rv = True
        elif self.first_half_complete and cube.pos >= self.size:
            rv = True
        # place cube in destination space
        self.spaces[cube.pos].append(cube)
        # stats
        cube.stats.steps_total += 1
        # return true if the cube reached the end
        return rv
    
    def stack_cube_on_top(self, cube: Cube):
        assert cube in self.spaces[cube.pos]
        # remove cube fromm space
        self.spaces[cube.pos].remove(cube)
        # append cube on top
        self.spaces[cube.pos].append(cube)
    
    def get_place(self, cube: Cube):
        place = 1
        for space in reversed(self.spaces):
            for other_cube in space:
                if id(cube) == id(other_cube):
                    return place
                else:
                    place += 1
        raise ValueError("Cube not found on board.")
    
    def get_standings(self):
        rv = list()
        for space in reversed(self.spaces):
            for cube in space:
                rv.append(cube)
        return rv
