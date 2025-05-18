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

    for cube in race.cubes:
        print(f"{cube.__class__.__name__} in position {cube.pos}")


if __name__ == "__main__":
    main()
