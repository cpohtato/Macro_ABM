from .market import *

class MarketManager():

    def __init__(self, numMarkets: int):
        
        self.listMarkets: list[Market] = []
        for i in range(numMarkets):
            self.listMarkets.append(Market(i))

    def estimateProfits(self):
        
        listProfits: list[float] = []
        for market in self.listMarkets:
            listProfits.append(market.estimateProfit())

        return listProfits

    def settle(self):
        pass