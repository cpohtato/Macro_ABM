from ..utils import *

ENTREPRENEURIAL_RELUCTANCE = 0.25
WAGE_NORM_STD_DEV = 0.1

class Pop():

    def __init__(self, id: int):
        
        self.id: int = id

        self.ownsFirm: bool = False
        self.ownedFirmType: int = -1

    def modifyProfits(self, listProfits: list[float]):

        listModifiedProfits = listProfits.copy()
        for outputType in range(NUM_MARKET_TYPES):
            if outputType != TYPE_LABOUR: listModifiedProfits[outputType] *= 1 - ENTREPRENEURIAL_RELUCTANCE

        return listModifiedProfits

    def chooseOutputType(self, listProfits: list[float]):
        listModifiedProfits = self.modifyProfits(listProfits)
        return random.choices(range(NUM_MARKET_TYPES), listModifiedProfits)

    def createNewFirm(self, outputType: int):
        self.ownsFirm = True
        self.ownedFirmType = outputType

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
            else: self.createNewFirm(outputType)

        return [self.id, outputType, firmExists, price]

