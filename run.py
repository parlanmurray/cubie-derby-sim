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
        row.append(cube_stats.won_both / cube_stats.first_half_wins)
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
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", type=int, default=10000)
    parser.add_argument("-j", "--jobs", type=int, default=10)
    parser.add_argument("--cubes", type=str, help="comma separated list of cube names", default="Zani,Cantarella,Phoebe,Brant,Roccia,Cartetheyia")

    args = parser.parse_args()

    stats_dict = dict()
    cube_name_list = args.cubes.split(",")

    for cube_name in cube_name_list:
        stats_dict[cube_name] = StatsAggregator()

    for _ in range(args.n):
        cubes_list = [cubes[cube_name]() for cube_name in cube_name_list]
        race = Race(cubes_list)

        race.run_half()
        first_half_standings = race.board.get_standings()
        race.run_half()
        final_standings = race.board.get_standings()

        # aggregate stats
        for cube in final_standings:
            stats_dict[cube.__class__.__name__].accumulate(cube.stats)
        stats_dict[first_half_standings[0].__class__.__name__].first_half_wins += 1
        stats_dict[final_standings[0].__class__.__name__].second_half_wins += 1
        if id(first_half_standings[0]) == id(final_standings[0]):
            stats_dict[final_standings[0].__class__.__name__].won_both += 1

    print(f"Results - {args.n} runs")
    print_stats(stats_dict)


if __name__ == "__main__":
    main()
