from ..utils import *
from ..markets.marketManager import *
from ..firms.firmManager import *
from ..pops.popManager import *

class Govt():

    def __init__(self):

        self.funds: float = 0.0

        self.producePurchased: int = 0
        self.servicesPurchased: int = 0
        self.metalPurchased: int = 0

    def settle(self):

        self.producePurchased: int = 0
        self.servicesPurchased: int = 0
        self.metalPurchased: int = 0

    def levyIncomeTax(self, pops: PopManager):

        self.settle()

        self.funds += pops.levyIncomeTax() 

    def canAfford(self, markets: MarketManager, goodType: int):

        lowestPriceAvailable = markets.lowestPriceAvailable(goodType)
        if (lowestPriceAvailable >= 0.0):
            return (self.funds > lowestPriceAvailable)
        return False

    def buyFromMarket(self, markets: MarketManager, goodType: int):

        price = markets.buyGood(goodType)
        self.funds -= price

    def feedStarvingPops(self, pops: PopManager, markets: MarketManager):

        numStarvingPops: int = pops.findNumStarvingPops()
        foodPurchased: int = 0

        while (foodPurchased < numStarvingPops):
            if (self.canAfford(markets, TYPE_PRODUCE)):
                self.buyFromMarket(markets, TYPE_PRODUCE)
                self.producePurchased += 1
                foodPurchased += 1
            else: break

        pops.feedStarvingPops(foodPurchased) 

    def buyPublicGoods(self, pops: PopManager, markets: MarketManager):

        population: int = pops.findNumPops()
        targetServices: int = round(population * SERVICES_PER_POP)
        servicesPurchased: int = 0

        while (servicesPurchased < targetServices):
            if (self.canAfford(markets, TYPE_SERVICES)):
                self.buyFromMarket(markets, TYPE_SERVICES)
                self.servicesPurchased += 1
                servicesPurchased += 1
            else: break

        targetMetal: int = round(population * METAL_PER_POP)
        metalPurchased: int = 0

        while (metalPurchased < targetMetal):
            if (self.canAfford(markets, TYPE_METAL)):
                self.buyFromMarket(markets, TYPE_METAL)
                self.metalPurchased += 1
                metalPurchased += 1
            else: break