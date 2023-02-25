from .firm import *

class FirmManager():

    def __init__(self):
        
        self.listFirms: list[Firm] = []

    def makeNewFirmsFromDecisionMap(self, popDecisionMap: list[list]):

        for decision in popDecisionMap:
            if ((decision[DECISION_GOOD_TYPE_INDEX] != TYPE_LABOUR) & (not decision[DECISION_FIRM_EXISTS_INDEX])):
                self.createNewFirm(decision)

    def createNewFirm(self, popDecision: list):

        firmId = self.findNewFirmId()
        ownerId = popDecision[DECISION_ID_INDEX]
        goodType = popDecision[DECISION_GOOD_TYPE_INDEX]
        initInvestment = popDecision[DECISION_PRICE_INDEX]
        self.listFirms.append(Firm(firmId, ownerId, goodType, initInvestment))

    def findNewFirmId(self):

        newID = 0
        while (True):
            if (self.firmIdExists(newID)): newID += 1
            else: return newID

    def firmIdExists(self, id: int):

        for firm in self.listFirms:
            if (firm.getFirmId() == id): return True
        return False

    def produce(self, marketManager: MarketManager):
        
        numFirms = len(self.listFirms)
        randOrder = list(range(numFirms))
        random.shuffle(randOrder)

        for idx in randOrder:
            self.listFirms[idx].produceOutput(marketManager) 

    def payDividends(self, id: int):

        for firm in self.listFirms: 
            if (id == firm.getOwnerId()): return firm.payDividend() 
        return 0.0

    def settle(self, marketManager: MarketManager):
        
        for firm in self.listFirms:
            firm.settle(marketManager)

    def closeUnprofitableFirms(self, pManager):

        from ..pops import popManager 

        survivingFirms = []

        for firm in self.listFirms:
            if (firm.getMonthsUnprofitable() >= UNPROFITABLE_MONTH_LIMIT):
                ownerId, funds = firm.close()
                pManager.closeOwnedFirm(ownerId, funds) 
            else: survivingFirms.append(firm)

        self.listFirms = survivingFirms.copy()

    def numFirmsBySector(self):

        numFirms = [0] * NUM_GOOD_TYPES
        for firm in self.listFirms:
            numFirms[firm.getGoodType()] += 1
        return numFirms

    def avgProfitsBySector(self, numFirms: list[int]):

        listProfits = [0.0] * NUM_GOOD_TYPES
        for firm in self.listFirms:
            listProfits[firm.getGoodType()] += firm.getPrevProfit()

        for goodType in range(NUM_GOOD_TYPES):
            if (numFirms[goodType] > 0): listProfits[goodType] /= numFirms[goodType]
            else: listProfits[goodType] = 0.0

        return listProfits

    def logMonth(self, month: int, econName: str):

        numFirms: list[int] = self.numFirmsBySector()
        listProfits: list[float] = self.avgProfitsBySector(numFirms)

        with open("logs/" + econName +"/firms.txt", "a") as logFile:
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")
            for goodType in range(1, NUM_GOOD_TYPES):
                logFile.write(DICT_GOOD_TYPES[goodType] + ": " + 
                              str(numFirms[goodType]) + " firms, avg. profit $" +
                              f"{listProfits[goodType]:.2f}")
                logFile.write("\n")
            logFile.write("\n")
            logFile.write("\n")

        return numFirms, listProfits