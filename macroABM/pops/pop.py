from ..utils import *
from ..markets.marketManager import *
from ..firms.firmManager import *

ENTREPRENEURIAL_RELUCTANCE = 0.6
WAGE_NORM_STD_DEV = 0.03

class Pop():

    def __init__(self, id: int):
        
        self.id: int = id

        self.ownsFirm: bool = False
        self.ownedFirmType: int = -1

        self.funds: float = INIT_FUNDS_PER_POP
        self.currIncome: float = 0.0

        self.producePreference = random.normalvariate(DICT_PREFERENCE_MEAN[TYPE_PRODUCE],
                                                      DICT_PREFERENCE_STD_DEV[TYPE_PRODUCE])
        self.servicesPreference = random.normalvariate(DICT_PREFERENCE_MEAN[TYPE_SERVICES],
                                                       DICT_PREFERENCE_STD_DEV[TYPE_SERVICES])
        self.cgPreference = random.normalvariate(DICT_PREFERENCE_MEAN[TYPE_CONSUMER_GOODS],
                                                 DICT_PREFERENCE_STD_DEV[TYPE_CONSUMER_GOODS])

        self.currBundle: list[int] = [0] * NUM_GOOD_TYPES

    def roiToProfit(self, roi: float):

        investment = self.funds * (1 - SAVINGS_RATE)
        return roi * investment * (1 - ENTREPRENEURIAL_RELUCTANCE)

    def modifyProfits(self, listProfits: list[float]):

        listModifiedProfits = listProfits.copy()
        for outputType in range(NUM_GOOD_TYPES):
            if outputType != TYPE_LABOUR: listModifiedProfits[outputType] = self.roiToProfit(listProfits[outputType])
            else: listModifiedProfits[outputType] *= LABOUR_PER_POP

            if (listModifiedProfits[outputType] < 0.0): listModifiedProfits[outputType] = 0.0

        if (sum(listModifiedProfits) == 0.0): 
            listModifiedProfits = [1.0] * NUM_GOOD_TYPES
            listModifiedProfits[TYPE_LABOUR] = 0.0
        
        return listModifiedProfits

    def chooseOutputType(self, listProfits: list[float]):
        listModifiedProfits = self.modifyProfits(listProfits)
        return random.choices(range(NUM_GOOD_TYPES), listModifiedProfits)[0]

    def createNewFirm(self, outputType: int):
        self.ownsFirm = True
        self.ownedFirmType = outputType
        investment = self.funds * INVESTMENT_RATE
        self.funds -= investment
        return investment

    def priceLabour(self, baseWage: float):
        sigma = baseWage * WAGE_NORM_STD_DEV
        return random.normalvariate(baseWage, sigma) * (1 + MONTHLY_INFLATION)

    def chooseOutput(self, listProfits: list[float]):

        self.currBundle = [0] * NUM_GOOD_TYPES

        firmExists: bool = False
        price: float = -1.0
        outputType: int = -1

        if (self.ownsFirm): 
            outputType = self.ownedFirmType
            firmExists = True
        else:
            outputType = self.chooseOutputType(listProfits)
            
            if (outputType == TYPE_LABOUR): price = self.priceLabour(listProfits[TYPE_LABOUR])
            else: price = self.createNewFirm(outputType)

        # outputType: type of good
        # firmExists: if owned firm already exists
        # price:      if (output == labour): price == asking price for this pop's labour
        #             else:
        #                 if (firmExists == True): price means nothing
        #                 else:                    price == starting investment into new firm

        return [self.id, outputType, firmExists, price]

    def getOwnsFirm(self):

        return self.ownsFirm

    def getOwnedFirmType(self):

        return self.ownedFirmType

    def getId(self):

        return self.id

    def receiveIncome(self, income: float):

        self.currIncome = income
        self.funds += income

    def utilityFunction(self, bundle: list[int]):

        produceUtility = math.sqrt(self.producePreference * bundle[TYPE_PRODUCE])
        servicesUtility = math.sqrt(self.servicesPreference * bundle[TYPE_SERVICES] + 1)
        cgUtility = math.sqrt(self.cgPreference * bundle[TYPE_CONSUMER_GOODS] + 1)
        return produceUtility * servicesUtility * cgUtility

    def getMargUtility(self):

        listMU: list[float] = [0] * NUM_GOOD_TYPES
        currBundle = self.currBundle
        currUtility: float = self.utilityFunction(currBundle)
        for goodType in range(NUM_GOOD_TYPES):
            newBundle = currBundle.copy()
            newBundle[goodType] += 1
            newUtility: float = self.utilityFunction(newBundle)
            listMU[goodType] = newUtility - currUtility
        return listMU

    def getMargUtilityRatio(self, listMenu: list[float]):

        listMU = self.getMargUtility()
        listMUP = [0] * NUM_GOOD_TYPES
        for goodType in range(NUM_GOOD_TYPES):
            listMUP[goodType] = listMU[goodType] / listMenu[goodType]
        return listMUP

    def canAfford(self, budget: float, spent: float, typeChoice: int, marketManager: MarketManager):

        remaining: float = budget - spent
        price = marketManager.lowestPriceAvailable(typeChoice)
        return (remaining >= price)

    def consumeGoods(self, marketManager: MarketManager):

        budget: float = self.funds * (1 - SAVINGS_RATE)
        spent: float = 0.0

        while (True):

            listMenu = marketManager.getMenu()
            listMUP = self.getMargUtilityRatio(listMenu)
            typeChoice = np.argmax(listMUP)
            
            if (listMUP[typeChoice] > 0) & self.canAfford(budget, spent, typeChoice, marketManager): 
                spent += marketManager.buyGood(typeChoice)
                self.currBundle[typeChoice] += 1
            else: break

        self.funds -= spent

    def settle(self):

        self.currIncome = 0
        # self.currBundle = [0] * NUM_GOOD_TYPES

    def closeOwnedFirm(self, firmFunds: float):

        self.funds += firmFunds
        self.ownsFirm = False
        self.ownedFirmType = -1

    def payIncomeTax(self):

        incomeTax: float = self.currIncome * INCOME_TAX_RATE
        self.funds -= incomeTax
        return incomeTax
        

