from ..utils import *
from .sellOrder import *

WAGE_VISCOSITY = 0.03
GOOD_PROFIT_INCREASE = 0.05
ESTIMATED_BASE_ROI = 0.5

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
            clearanceRatio: float = float(self.prevNumTrades) / float(self.prevNumSupplied)
            if (clearanceRatio >= EMPLOYMENT_RATE): return (self.prevAvgTradedPrice * (1 + WAGE_VISCOSITY))
            else: return (self.prevAvgTradedPrice * (1 - WAGE_VISCOSITY))
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
        return self.prevAvgTradedPrice * ESTIMATED_BASE_ROI

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