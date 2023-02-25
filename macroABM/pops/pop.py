from ..utils import *

ENTREPRENEURIAL_RELUCTANCE = 0.25
WAGE_NORM_STD_DEV = 0.1

class Pop():

    def __init__(self, id: int):
        
        self.id: int = id

        self.ownsFirm: bool = False
        self.ownedFirmType: int = -1

        self.funds:float = INIT_FUNDS_PER_POP

    def roiToProfit(self, roi: float):

        investment = self.funds * (1 - SAVINGS_RATE)
        return roi * investment * (1 - ENTREPRENEURIAL_RELUCTANCE)

    def modifyProfits(self, listProfits: list[float]):

        listModifiedProfits = listProfits.copy()
        for outputType in range(NUM_MARKET_TYPES):
            if outputType != TYPE_LABOUR: listModifiedProfits[outputType] = self.roiToProfit(listProfits[outputType])

        return listModifiedProfits

    def chooseOutputType(self, listProfits: list[float]):
        listModifiedProfits = self.modifyProfits(listProfits)
        return random.choices(range(NUM_MARKET_TYPES), listModifiedProfits)

    def createNewFirm(self, outputType: int):
        self.ownsFirm = True
        self.ownedFirmType = outputType
        investment = self.funds * (1 - SAVINGS_RATE)
        self.funds -= investment
        return investment

    def priceLabour(self, baseWage: float):
        sigma = baseWage * WAGE_NORM_STD_DEV
        return random.normalvariate(baseWage, sigma)

    def chooseOutput(self, listProfits: list[float]):

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

        

