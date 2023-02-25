from ..utils import *
from ..markets.marketManager import *

PRICE_VISCOSITY = 0.05
PRICE_STD_DEV = 0.08
STD_DEV_FOR_90_PERCENT_CLEARANCE = 1.28

LABOUR_PROD_MEAN = 1.0
LABOUR_PROD_STD_DEV = 0.05
CAPITAL_PROD_MEAN = 1.0
CAPITAL_PROD_STD_DEV = 0.05

MARKUP_FACTOR = 1.5

class Firm():

    def __init__(self, firmId: int, ownerId: int, goodType: int, initInvestment: float):
        
        self.firmId = firmId
        self.ownerId = ownerId
        self.goodType = goodType
        self.funds = initInvestment

        self.currCapital: int = 0
        self.currLabour: int = 0

        self.labourFactor: float = random.normalvariate(LABOUR_PROD_MEAN, LABOUR_PROD_STD_DEV)
        self.capitalFactor: float = random.normalvariate(CAPITAL_PROD_MEAN, CAPITAL_PROD_STD_DEV)

        self.currDividends: float = 0.0
        self.currWages: float = 0.0
        self.currRawMaterialCosts: float = 0.0
        self.currRevenue: float = 0.0

        self.prevProfit: float = 0.0
        self.monthsUnprofitable: int = 0

    def getFirmId(self):
        
        return self.firmId

    def priceFloor(self, price):

        if (price <= PRICE_FLOOR): return PRICE_FLOOR
        return price

    def priceGouge(self, highestTradedPrice: float):

        mu: float = highestTradedPrice * (1 + PRICE_VISCOSITY)
        sigma: float = highestTradedPrice * PRICE_STD_DEV
        newPrice: float = random.normalvariate(mu, sigma)

        if (newPrice < highestTradedPrice): newPrice = highestTradedPrice
        newPrice = self.priceFloor(newPrice)

        return newPrice

    def equilibriumPricing(self, highestTradedPrice: float, avgTradedPrice: float):

        mu: float = highestTradedPrice
        sigma: float = avgTradedPrice * PRICE_STD_DEV
        newPrice: float = random.normalvariate(mu, sigma)
        newPrice = self.priceFloor(newPrice)
        return newPrice

    def competitivePricing(self, highestTradedPrice: float, avgTradedPrice: float):

        mu: float = (highestTradedPrice + avgTradedPrice) / 2
        sigma: float = avgTradedPrice * PRICE_STD_DEV
        newPrice: float = random.normalvariate(mu, sigma)
        newPrice = self.priceFloor(newPrice)
        return newPrice

    def choosePriceOfGoods(self, marketManager: MarketManager):

        highestTradedPrice = marketManager.getHighestTradedPrice(self.goodType)
        avgTradedPrice = marketManager.getAvgTradedPrice(self.goodType) 
        marketClearanceRatio = marketManager.getClearanceRatio(self.goodType)

        if (marketClearanceRatio == 1.00): 
            return self.priceGouge(highestTradedPrice)
        elif (marketClearanceRatio >= EQUILIBRIUM_CLEARANCE_RATE): 
            return self.equilibriumPricing(highestTradedPrice, avgTradedPrice)
        else: 
            return self.competitivePricing(highestTradedPrice, avgTradedPrice)

    def reserveDividends(self):

        self.currDividends = self.funds * DIVIDEND_RATE
        self.funds -= self.currDividends

    def productivityFunction(self, labourFactor: float, labour: int, capitalFactor: float, capital: int):

        labourProd = LABOUR_SCALE_FACTOR * math.sqrt(
                     labourFactor * 
                     ((labour + LABOUR_PER_POP) * PP_PER_LABOUR) / 
                     LABOUR_SCALE_FACTOR)

        capitalProd = CAPITAL_SCALE_FACTOR * math.sqrt(
                      capitalFactor * (capital + 1) /
                      CAPITAL_SCALE_FACTOR)

        return  labourProd * capitalProd

    def calcMPL(self):

        currProd: float = self.productivityFunction(self.labourFactor, self.currLabour, 1, 0)
        newProd: float = self.productivityFunction(self.labourFactor, self.currLabour + 1, 1, 0)
        return newProd - currProd

    def calcMargWagePerProd(self, marketManager: MarketManager):

        margProdLab = self.calcMPL()
        lowestWage = marketManager.lowestPriceAvailable(TYPE_LABOUR)
        availableFunds = self.funds - self.currDividends - self.currWages - self.currRawMaterialCosts
        if (lowestWage > availableFunds): return -1.0
        return lowestWage / margProdLab

    def calcMargProdInputCost(self, marketManager: MarketManager):

        #   TODO: some good types will require input goods for production
        return 0.0

    def calcMargProfitPerProd(self, goodPrice: float, marketManager: MarketManager):

        profit = goodPrice - self.calcMargProdInputCost(marketManager)
        return profit / DICT_GOOD_PP_COST[self.goodType]

    def hireLabour(self, marketManager: MarketManager):

        wage = marketManager.buyGood(TYPE_LABOUR) 
        self.currLabour += 1
        self.currWages += wage
        return True

    def chooseToBuyInputs(self, goodPrice: float, marketManager: MarketManager):

        if not (marketManager.goodAvailable(TYPE_LABOUR)): 
            return False

        wagePerProd = self.calcMargWagePerProd(marketManager)
        if (wagePerProd < 0.0): return False

        profitPerProd = self.calcMargProfitPerProd(goodPrice, marketManager)
        profitPerProd /= MARKUP_FACTOR

        if (profitPerProd > wagePerProd): return self.hireLabour(marketManager) 
        return False

    def convertInputsToOutput(self):

        totalPP = self.productivityFunction(self.labourFactor,
                                            self.currLabour,
                                            self.capitalFactor,
                                            self.currCapital)
        return math.floor(totalPP / DICT_GOOD_PP_COST[self.goodType])

    def maximiseProfit(self, goodPrice: float, marketManager: MarketManager):

        #   To hire, firm must make profit; condition given below:
        #   (output price) > (input cost) + (production points) * ((wage) / (marginal productivity))
        #   Where MP is marginal productivity and PP is production point cost, condition is:
        #   (MP / wage) > (PP / ((output price) - (input cost)))
        #   (MP / wage) is the MP-wage ratio (MPW)

        self.reserveDividends()

        while (True):
            if not (self.chooseToBuyInputs(goodPrice, marketManager)): break

        unitsProduced = self.convertInputsToOutput()
        totalCost: float = self.currDividends + self.currWages + self.currRawMaterialCosts
        self.funds -= totalCost

        return unitsProduced, totalCost

    def produceOutput(self, marketManager: MarketManager):
        
        goodPrice = self.choosePriceOfGoods(marketManager)
        unitsProduced, totalCost = self.maximiseProfit(goodPrice, marketManager)
        marketManager.moveGoodsToMarket(self.goodType, self.firmId, goodPrice, unitsProduced, totalCost)

    def payDividend(self):

        return self.currDividends

    def getOwnerId(self):

        return self.ownerId

    def settle(self, marketManager: MarketManager):

        self.currRevenue = marketManager.payRevenue(self.firmId, self.goodType)
        self.funds += self.currRevenue

        totalCosts = self.currDividends + self.currLabour + self.currRawMaterialCosts
        self.prevProfit = self.currRevenue - totalCosts
        if (self.prevProfit < 0): self.monthsUnprofitable += 1
        else: self.monthsUnprofitable = 0

        self.currLabour = 0
        self.currDividends = 0.0
        self.currWages = 0.0
        self.currRawMaterialCosts = 0.0
        self.currRevenue = 0.0

    def getMonthsUnprofitable(self):

        return self.monthsUnprofitable

    def close(self):

        return self.ownerId, self.funds

    def getGoodType(self):

        return self.goodType

    def getPrevProfit(self):

        return self.prevProfit