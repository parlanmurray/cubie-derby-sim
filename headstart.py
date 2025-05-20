import argparse

from tabulate import tabulate

from derbysim import *

cubes = {"Zani": Zani, "Cantarella": Cantarella, "Phoebe": Phoebe, "Brant": Brant, "Roccia": Roccia, "Cartetheyia": Cartetheyia, "Calcharo": Calcharo, "Carlotta": Carlotta, "Camellya": Camellya, "Jinhsi": Jinhsi}


def print_stats(stats):
    table = list()
    for cube_str, cube_stats in stats.items():
        row = list()
        row.append(cube_str)
        row.append(cube_stats.first_half_wins + cube_stats.second_half_wins)
        row.append(cube_stats.first_half_wins)
        row.append(cube_stats.second_half_wins)
        if cube_stats.first_half_wins:
            row.append(cube_stats.won_both / cube_stats.first_half_wins)
        else:
            row.append('N/A')
        row.append(cube_stats.steps_total)
        row.append(cube_stats.steps_base)
        row.append(cube_stats.steps_carried)
        row.append(cube_stats.ability_triggered)
        table.append(row)
    print(tabulate(table, headers=["Name", "Total Wins", "1st Half Wins", "2nd Half Wins", "Conversion Rate", "Total Steps", "Steps Base", "Steps Carried", "Ability Triggers"]))


class StatsAggregator:
    def __init__(self):
        self.steps_total: int = 0
        self.steps_base: int = 0
        self.ability_triggered: int = 0
        self.turns: int = 0
        self.steps_carried: int = 0
        self.steps_carrying_others: int = 0
        self.first_half_wins = 0
        self.second_half_wins = 0
        self.won_both = 0
    
    def accumulate(self, single: Stats):
        self.steps_total += single.steps_total
        self.steps_base += single.steps_base
        self.ability_triggered += single.ability_triggered
        self.turns += single.turns
        self.steps_carried += single.steps_carried
        self.steps_carrying_others += single.steps_carrying_others


def main():
    stats_dict = dict()
    stats_dict['Calcharo'] = StatsAggregator()
    stats_dict['Carlotta'] = StatsAggregator()
    stats_dict['Jinhsi'] = StatsAggregator()
    stats_dict['Camellya'] = StatsAggregator()

    for _ in range(10000):
        calc = Calcharo()
        carlotta = Carlotta()
        jinny = Jinhsi()
        cammy = Camellya()

        calc.pos = 24
        jinny.pos = 24
        carlotta.pos = 20
        cammy.pos = 20

        race = Race([calc, carlotta, jinny, cammy])
        race.board.spaces[0] = list()
        race.board.first_half_complete = True
        race.board.spaces[24] = [calc, jinny]
        race.board.spaces[20] = [carlotta, cammy]

        race.run_half()
        final_standings = race.board.get_standings()

        for cube in final_standings:
            stats_dict[cube.__class__.__name__].accumulate(cube.stats)
        stats_dict['Jinhsi'].first_half_wins += 1
        stats_dict[final_standings[0].__class__.__name__].second_half_wins += 1
        if final_standings[0].__class__.__name__ == 'Jinhsi':
            stats_dict['Jinhsi'].won_both += 1

    print(f"Results - 10000 runs")
    print_stats(stats_dict)

if __name__ == "__main__":
    main()
