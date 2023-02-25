from .firm import *

class FirmManager():

    def __init__(self):
        
        self.listFirms: list[Firm] = []

    def makeNewFirmsFromDecisionMap(self, popDecisionMap: list[list]):

        for decision in popDecisionMap:
            if ((decision[DECISION_GOOD_TYPE_INDEX] != TYPE_LABOUR) & ~(decision[DECISION_FIRM_EXISTS_INDEX])):
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

    def produce(self):
        pass

    def settle(self):
        pass