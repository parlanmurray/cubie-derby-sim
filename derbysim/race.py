import random

from tabulate import tabulate

from . import Board

class RaceCompleteException(Exception):
    pass

class Race:
    def __init__(self, cubes: list):
        self.cubes = cubes
        self.board = Board()
        self.board.spaces[0] = self.cubes.copy()

    def run_half(self):
        # reset all cubes
        for cube in self.cubes:
            cube.reset()
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
            cube.stats.turns += 1

            # roll
            roll = cube.roll(
                self.board.get_above(cube),
                self.board.get_below(cube),
                i + 1,
                len(self.cubes),
                self.board.get_place(cube)
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
                race_complete = False
                for ma in actions:
                    if not ma.carried:
                        ma.subject.stats.steps_base += 1
                    else:
                        ma.subject.stats.steps_carried += 1
                    if ma.carrying:
                        ma.subject.stats.steps_carrying_others += 1
                    if self.board.move_cube(ma.subject):
                        race_complete = True
                # we all cubes being carried need to move before we determine winner
                if race_complete:
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

        # end of turn action
        for cube in self.cubes:
            sa = cube.turn_end_action(
                self.board.get_above(cube),
                self.board.get_below(cube)
            )
            if sa:
                self.board.stack_cube_on_top(sa.subject)

    def print_results(self):
        standings = self.board.get_standings()
        for i, cube in enumerate(standings):
            print(f"{i+1} {cube.__class__.__name__}")

    def print_stats(self):
        standings = self.board.get_standings()
        table = list()
        for i, cube in enumerate(standings):
            row = list()
            row.append(cube.__class__.__name__)
            row.append(i+1)
            row.append(cube.pos)
            row.append(cube.stats.turns)
            row.append(cube.stats.steps_total)
            row.append(cube.stats.steps_base)
            row.append(cube.stats.steps_carried)
            row.append(cube.stats.ability_triggered)
            row.append(cube.stats.steps_carrying_others)
            table.append(row)
        print(tabulate(table, headers=["Name", "Place", "Position", "Turns", "Steps Total", "Steps Base", "Steps Carried", "Ability Triggered", "Steps Carrying Others"]))
