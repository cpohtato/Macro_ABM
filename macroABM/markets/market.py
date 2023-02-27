from ..utils import *
from .sellOrder import *

WAGE_VISCOSITY = 0.05
GOOD_PROFIT_INCREASE = 0.05
ESTIMATED_BASE_ROI = 0.25

class Market():

    def __init__(self, type: int):
        
        self.marketType: int = type

        self.prevNumSellers: int = 0
        self.prevNumSupplied: int = 0
        self.prevNumTrades: int = 0
        self.prevAvgTradedPrice: float = 0
        self.prevHighestTradedPrice: float = 0

        self.prevFundsInvested: float = 0
        self.prevTotalRevenue: float = 0

        if (self.marketType == TYPE_LABOUR): self.initLabourMarket()
        else: self.initGoodMarket()

        self.listSellOrders: list[SellOrder] = []

    def initLabourMarket(self):

        self.prevNumSellers = round(INIT_LABOUR_RATIO * INIT_POPS)
        self.prevNumSupplied = self.prevNumSellers
        self.prevNumTrades = round(self.prevNumSupplied * EMPLOYMENT_RATE)
        self.prevAvgTradedPrice = DICT_INIT_AVG_PRICES[TYPE_LABOUR]
        self.prevHighestTradedPrice = self.prevAvgTradedPrice * (1 + INIT_PRICE_MAX_SPREAD)

    def initGoodMarket(self):

        self.prevNumSellers = 0
        self.prevNumSupplied = 0
        self.prevNumTrades = 0
        self.prevAvgTradedPrice = DICT_INIT_AVG_PRICES[self.marketType]
        self.prevHighestTradedPrice = self.prevAvgTradedPrice * (1 + INIT_PRICE_MAX_SPREAD)

    def estimateCompetitiveWage(self):
        
        if (self.prevNumSellers > 0):
            clearanceRatio = self.getClearanceRatio()
            if (clearanceRatio >= EMPLOYMENT_RATE): return (self.prevAvgTradedPrice * (1 + WAGE_VISCOSITY))
            else: return (self.prevAvgTradedPrice)
        else:
            #   TODO: remember to carry prevAvgTradedPrice from last tick if no trades occur in current tick in settlement
            self.prevAvgTradedPrice *= (1 + WAGE_VISCOSITY)
            return self.prevAvgTradedPrice

    def estimateExistingMarketROI(self):
        totalProfit = self.prevTotalRevenue - self.prevFundsInvested
        roi = totalProfit / self.prevFundsInvested
        return roi

    def estimateNewMarketROI(self):

        if (self.prevAvgTradedPrice == 0.0): 
                self.prevAvgTradedPrice = 0.1
        else:
            self.prevAvgTradedPrice *= (1 + GOOD_PROFIT_INCREASE)
        return self.prevAvgTradedPrice * ESTIMATED_BASE_ROI / DICT_GOOD_PP_COST[self.marketType]

    def estimateFirmROI(self):
        
        if (self.prevFundsInvested > 0):
            return self.estimateExistingMarketROI()
        else:
            return self.estimateNewMarketROI()    

    def estimateProfit(self):
        
        if (self.marketType == TYPE_LABOUR): return self.estimateCompetitiveWage()
        else: return self.estimateFirmROI()

    def createSellOrder(self, id: int, price: float, qty: int, cost: float):

        self.listSellOrders.append(SellOrder(id, price, qty, cost))

    def getPrevHighestTradedPrice(self):

        return self.prevHighestTradedPrice

    def getPrevAvgTradedPrice(self):

        return self.prevAvgTradedPrice

    def getClearanceRatio(self):

        if (self.prevNumSupplied > 0): return float(self.prevNumTrades) / float(self.prevNumSupplied)
        else: return 1.0

    def searchLowestAvailablePrice(self):

        lowestPrice: float = -1.0
        lowestPriceIndex: int = -1

        for index in range(len(self.listSellOrders)):
            if (self.listSellOrders[index].unitsAvailable() & 
                ((self.listSellOrders[index].getPrice() < lowestPrice) | 
                (lowestPrice == -1.0))):
                    lowestPrice = self.listSellOrders[index].getPrice()
                    lowestPriceIndex = index

        return lowestPrice, lowestPriceIndex

    def getLowestAvailablePrice(self):

        if (len(self.listSellOrders) > 0): return self.searchLowestAvailablePrice()
        return -1.0, -1

    def buyLowest(self):

        lowestPrice, lowestPriceIndex = self.searchLowestAvailablePrice()
        if (lowestPriceIndex >= 0):
            self.listSellOrders[lowestPriceIndex].makePurchase() 
        return lowestPrice

    def searchAvailableGoods(self):

        for sellOrder in self.listSellOrders:
            if (sellOrder.unitsAvailable()): return True
        return False

    def checkIfAvailable(self):

        if (len(self.listSellOrders) > 0): return self.searchAvailableGoods()
        return False

    def payRevenue(self, id: int):

        for order in self.listSellOrders: 
            if (id == order.getId()): return order.getTotalRevenue()
        return 0.0

    def getTotalSupply(self):

        sum: int = 0
        for sellOrder in self.listSellOrders:
            sum += sellOrder.getQtySupplied()
        return sum

    def getTotalCosts(self):

        sum: float = 0.0
        for sellOrder in self.listSellOrders:
            sum += sellOrder.getCost()
        return sum

    def getTotalSold(self):

        sum: int = 0
        for sellOrder in self.listSellOrders:
            sum += sellOrder.getQtySold()
        return sum

    def getTotalRevenue(self):

        sum: float = 0.0
        for sellOrder in self.listSellOrders:
            sum += sellOrder.getTotalRevenue()
        return sum

    def getAvgTradedPrice(self):

        if (self.prevNumTrades > 0): return self.prevTotalRevenue / self.prevNumTrades
        return self.prevAvgTradedPrice

    def findHighestTradedPrice(self):

        highestTradedPrice: float = -1.0
        for sellOrder in self.listSellOrders:
            if ((sellOrder.getQtySold() > 0) & (sellOrder.getPrice() > highestTradedPrice)): 
                highestTradedPrice = sellOrder.getPrice()
        return highestTradedPrice

    def settle(self):

        #   Like this for readability not efficiency
        self.prevNumSellers = len(self.listSellOrders)
        self.prevNumSupplied = self.getTotalSupply()
        self.prevFundsInvested = self.getTotalCosts()
        self.prevNumTrades = self.getTotalSold()
        self.prevTotalRevenue = self.getTotalRevenue()

        self.prevAvgTradedPrice = self.getAvgTradedPrice()
        self.prevHighestTradedPrice = self.findHighestTradedPrice()

        self.listSellOrders = []

    def getMarketType(self):

        return self.marketType

    def getPrevNumTrades(self):

        return self.prevNumTrades