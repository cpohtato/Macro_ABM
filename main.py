from macroABM import *

def main():

    #   Create some country
    arcadia = NationalEconomy("arcadia", INIT_POPS)
    # byzantium = NationalEconomy("byzantium", INIT_POPS)
    
    arcadia.simulate(SIM_LENGTH)
    # byzantium.simulate(SIM_LENGTH)

if (__name__ == "__main__"):
    main()