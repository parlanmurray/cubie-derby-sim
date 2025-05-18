from derbysim import *

def main():
    zani = Zani()
    cantarella = Cantarella()
    phoebe = Phoebe()
    brant = Brant()
    roccia = Roccia()
    carte = Cartetheyia()
    race = Race([zani, cantarella, phoebe, brant, roccia, carte])

    # start race
    race.run_half()
    print("first half")
    race.print_stats()
    print("final")
    race.run_half()
    race.print_stats()


if __name__ == "__main__":
    main()
