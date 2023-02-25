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

    def makeLabourAvailable(self, decisionMap: list[list]):

        for decision in decisionMap:
            if (decision[DECISION_GOOD_TYPE_INDEX] == TYPE_LABOUR): 
                self.listMarkets[TYPE_LABOUR].createSellOrder(
                    decisionMap[DECISION_ID_INDEX], decisionMap[DECISION_PRICE_INDEX], 1, 0.0)

    def settle(self):
        pass