import random

from . import Board

class RaceCompleteException(Exception):
    pass

class Race:
    def __init__(self, cubes: list):
        self.cubes = cubes
        self.board = Board()
        self.board.spaces[0] = self.cubes.copy()

    def run_half(self):
        try:
            while True:
                self.round()
        except RaceCompleteException:
            pass

    def round(self):
        # random action order
        random.shuffle(self.cubes)

        # perform each cube's turn
        for i, cube in enumerate(self.cubes):
            # roll
            roll = cube.roll(
                self.board.get_above(cube),
                self.board.get_below(cube),
                i + 1,
                len(self.cubes)
            )

            # pre move
            cube.pre_move_action(
                self.board.get_above(cube),
                self.board.get_below(cube),
                i + 1,
                len(self.cubes)
            )

            for _ in range(roll):
                # take a step
                actions = cube.step(
                    self.board.get_above(cube),
                    self.board.get_below(cube),
                    i + 1,
                    len(self.cubes)
                )
                for ma in actions:
                    if self.board.move_cube(ma.subject):
                        raise RaceCompleteException

                # per step action
                cube.per_space_action(
                    self.board.get_above(cube),
                    self.board.get_below(cube),
                    i + 1,
                    len(self.cubes)
                )

            # post move
            cube.post_move_action(
                self.board.get_above(cube),
                self.board.get_below(cube),
                i + 1,
                len(self.cubes),
                self.board.get_place(cube)
            )

            # check if the race is over
            if cube.pos > 22:
                raise RaceCompleteException
