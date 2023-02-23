from .market import *

class NationalEconomy():

    def __init__(self, initPops: int):
        
        self.generateInitPops(initPops)
        self.generateMarkets(NUM_MARKET_TYPES)

    def generateInitPops(self, initPops):

        self.listPops: list[Pop] = []

        for i in range(initPops):
            self.listPops.append(Pop(i))

    def generateMarkets(self, numMarkets: int):

        self.listMarkets: list[Market] = []

        for i in range(numMarkets):
            self.listMarkets.append(Market(i))
