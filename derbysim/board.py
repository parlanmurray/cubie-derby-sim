
from . import Cube

class Board:
    size = 23

    def __init__(self):
        self.spaces = list()
        for _ in range(self.size):
            self.spaces.append(list())

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
                rv.append(cube)
        return rv

    def move_cube(self, cube: Cube) -> bool:
        rv = False
        assert cube in self.spaces[cube.pos]
        # remove cube from current space
        self.spaces[cube.pos].remove(cube)
        # increment cubes' position
        cube.pos += 1
        if cube.pos >= self.size:
            rv = True
        cube.pos = cube.pos % self.size
        # place cube in destination space
        self.spaces[cube.pos].append(cube)
        # return true if the cube reached the end
        return rv
    
    def get_place(self, cube: Cube):
        place = 1
        for space in reversed(self.spaces):
            for other_cube in space:
                if id(cube) == id(other_cube):
                    return place
                else:
                    place += 1
        raise ValueError("Cube not found on board.")
