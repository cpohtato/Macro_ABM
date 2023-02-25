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
                    decision[DECISION_ID_INDEX], decision[DECISION_PRICE_INDEX], LABOUR_PER_POP, 0.0)

    def moveGoodsToMarket(self, goodType: int, firmId: int, price: float, qty: int, cost: float):
        self.listMarkets[goodType].createSellOrder(firmId, price, qty, cost)

    def getHighestTradedPrice(self, goodType: int):

        return self.listMarkets[goodType].getPrevHighestTradedPrice()

    def getAvgTradedPrice(self, goodType: int):

        return self.listMarkets[goodType].getPrevAvgTradedPrice()

    def getClearanceRatio(self, goodType: int):

        return self.listMarkets[goodType].getClearanceRatio()

    def lowestPriceAvailable(self, goodType: int):

        lowestPrice, _ = self.listMarkets[goodType].getLowestAvailablePrice() 
        return lowestPrice

    def buyGood(self, goodType: int):

        return self.listMarkets[goodType].buyLowest()

    def goodAvailable(self, goodType: int):

        return self.listMarkets[goodType].checkIfAvailable() 

    def settle(self):

        for market in self.listMarkets:
            market.settle()

    def payRevenue(self, id: int, goodType: int):

        return self.listMarkets[goodType].payRevenue(id)

    def getMenu(self):

        listMenu: list[float] = []
        for market in self.listMarkets:
            goodPrice, _ = market.getLowestAvailablePrice()
            listMenu.append(goodPrice)
        return listMenu

    def logMonth(self, month: int, econName: str):

        sales = [0] * NUM_GOOD_TYPES
        avgPrices = [0.0] * NUM_GOOD_TYPES

        with open("logs/" + econName +"/sales.txt", "a") as logFile:
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")
            for goodType in range(NUM_GOOD_TYPES):
                sales[goodType] = self.listMarkets[goodType].getPrevNumTrades()
                avgPrices[goodType] = self.listMarkets[goodType].getAvgTradedPrice()
                logFile.write(DICT_GOOD_TYPES[goodType] + ": " + 
                              str(sales[goodType]) + " sold @ $" +
                              f"{avgPrices[goodType]:.2f}" + " ea. avg.")
                logFile.write("\n")
            logFile.write("\n")
            logFile.write("\n")

        return sales, avgPrices