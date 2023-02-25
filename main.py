from macroABM import *

def main():

    #   Create some country
    arcadia = NationalEconomy("Arcadia", INIT_POPS)
    # byzantium = NationalEconomy("Byzantium", INIT_POPS)

    arcadia.simulate(SIM_LENGTH)
    # byzantium.simulate(SIM_LENGTH)

if (__name__ == "__main__"):
    main()