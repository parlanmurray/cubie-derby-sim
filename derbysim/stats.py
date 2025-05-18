from dataclasses import dataclass

@dataclass
class Stats:
    steps_total: int = 0
    steps_base: int = 0
    ability_triggered: int = 0
    turns: int = 0
    steps_carried: int = 0
    steps_carrying_others: int = 0
