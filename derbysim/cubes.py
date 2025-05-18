import random

from . import MoveAction, StackAction, Stats


class Cube:
    pos = 0
    first_step = True
    
    def __init__(self):
        self.stats = Stats()

    def roll(self, above: list, below: list, action_order: int, total_cubes: int):
        return random.randrange(1, 3)

    def step(self, above: list, below: list, action_order: int, total_cubes: int):
        actions = list()
        actions.append(MoveAction(self, carrying=len(above) > 0 and not self.first_step))
        if not self.first_step:
            for cube in above:
                actions.append(MoveAction(cube, carried=True))
        self.first_step = False
        return actions

    def pre_move_action(self, above: list, below: list, action_order: int, total_cubes: int):
        pass

    def per_space_action(self, above: list, below: list, action_order: int, total_cubes: int):
        pass

    def post_move_action(self, above: list, below: list, action_order: int, total_cubes: int, curr_place: int):
        pass

    def turn_end_action(self, above: list, below: list):
        pass

    def reset(self):
        pass

class Zani(Cube):
    skill_proc = False

    def __repr__(self):
        return f"Zani(pos={self.pos}, skill_proc={self.skill_proc})"
    
    def roll(self, above, below, action_order, total_cubes):
        # roll is either 1 or 3
        roll = 2
        while roll == 2:
            roll = random.randrange(1, 3)

        # if last turn skill activated, we move 2 extra spaces
        if self.skill_proc:
            roll += 2
            self.stats.ability_triggered += 1
            self.skill_proc = False
        return roll
        
    def post_move_action(self, above, below, action_order, total_cubes, curr_place):
        # check to see if skill activates for next round
        if above and random.randrange(0, 99) < 40:
            self.skill_proc = True
        else:
            self.skill_proc = False
        
    def reset(self):
        self.skill_proc = False


class Cantarella(Cube):
    triggered = False
    carry_below = False
    carried_cubes = list()

    def step(self, above: list, below: list, action_order: int, total_cubes: int):
        actions = list()
        
        # if we have triggered skill this turn, we need to move cubes we grabbed
        if self.carry_below:
            for cube in self.carried_cubes:
                actions.append(MoveAction(cube, carried=True))
        
        actions = actions + super().step(above, below, action_order, total_cubes)
        return actions

    def per_space_action(self, above, below, action_order, total_cubes):
        # check if we trigger skill
        if not self.triggered:
            if below:
                self.triggered = True
                self.carry_below = True
                self.carried_cubes = below
                self.stats.ability_triggered += 1

    def post_move_action(self, above, below, action_order, total_cubes, curr_place):
        self.carry_below = False

    def reset(self):
        self.triggered = False
        self.carry_below = False
        self.carried_cubes = list()


class Roccia(Cube):
    def roll(self, above, below, action_order, total_cubes):
        roll = random.randrange(1, 3)

        # if we are the last to move in this round, move 2 extra spaces
        if action_order == total_cubes:
            roll += 2
            self.stats.ability_triggered += 1

        return roll


class Phoebe(Cube):
    def roll(self, above, below, action_order, total_cubes):
        roll = random.randrange(1, 3)

        # 50% chance to move extra space
        if random.randrange(0, 99) < 50:
            roll += 1
            self.stats.ability_triggered += 1
        return roll


class Brant(Cube):
    def roll(self, above, below, action_order, total_cubes):
        roll = random.randrange(1, 3)

        # if we are moving first, move 2 extra spaces
        if action_order == 1:
            roll += 2
            self.stats.ability_triggered += 1

        return roll


class Cartetheyia(Cube):
    triggered = False

    def roll(self, above, below, action_order, total_cubes):
        roll = random.randrange(1, 3)

        if self.triggered and random.randrange(0, 99) < 60:
            roll += 2
        return roll

    def post_move_action(self, above, below, action_order, total_cubes, curr_place):
        if curr_place == total_cubes:
            self.triggered = True
            self.stats.ability_triggered += 1

    def reset(self):
        self.triggered = False

class Camellya(Cube):
    triggered = False

    def roll(self, above, below, action_order, total_cubes):
        roll = super().roll(above, below, action_order, total_cubes)
        if len(above) > 0 and random.randrange(0, 99) < 50:
            self.triggered = True
            self.stats.ability_triggered += 1
            count = len(above) + len(below)
            roll += count
        return roll
    
    def step(self, above, below, action_order, total_cubes):
        if self.triggered:
            return [MoveAction(self)]
        else:
            return super().step(above, below, action_order, total_cubes)
        

class Jinhsi(Cube):
    def turn_end_action(self, above, below):
        if len(above) > 0 and random.randrange(0, 99) < 40:
            self.stats.ability_triggered += 1
            return StackAction(self)
        return None
    

class Carlotta(Cube):
    def roll(self, above, below, action_order, total_cubes):
        roll = super().roll(above, below, action_order, total_cubes)
        if random.randrange(0, 99) < 28:
            self.stats.ability_triggered += 1
            roll = roll * 2
        return roll
    

class Calcharo(Cube):
    def roll(self, above, below, action_order, total_cubes):
        roll = super().roll(above, below, action_order, total_cubes)
        if action_order == total_cubes:
            roll += 3
            self.stats.ability_triggered += 1
        return roll
