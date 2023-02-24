from .markets.marketManager import *
from .pops.popManager import *
from .firms.firmManager import *
import os

class NationalEconomy():

    def __init__(self, econName: str, initPops: int):

        self.econName: str = econName
        self.pops: PopManager = PopManager(initPops)
        self.markets: MarketManager = MarketManager(NUM_MARKET_TYPES)
        self.firms: FirmManager = FirmManager()

    def simulate(self, numMonths: int):

        self.wipeLogs()

        for month in range(numMonths):
            self.stepMonth()
            self.logState(month)

        self.displayResults()

    def stepMonth(self):
        
        self.stepProductionPhase()
        self.stepTaxationPhase()
        self.stepConsumptionPhase()
        self.stepSettlementPhase()

    def stepProductionPhase(self):
        
        listProfits: list[float] = self.markets.estimateProfits()
        self.pops.produce()
        self.firms.produce()

    def stepTaxationPhase(self):
        pass

    def stepConsumptionPhase(self):
        
        # self.govtConsume()
        self.pops.consume()

    def stepSettlementPhase(self):
        
        self.pops.settle()
        self.firms.settle()
        self.markets.settle()

    def logState(self, month: int):
        pass

    def displayResults(self):
        pass

    def wipeLogs(self):

        path: str = "logs/" + self.econName 
        if not os.path.exists(path):
            os.makedirs(path)

        with open("logs/" + self.econName +"/firms.txt", "w") as logFile:
            logFile.write("")

        with open("logs/" + self.econName +"/sales.txt", "w") as logFile:
            logFile.write("")

        with open("logs/" + self.econName +"/jobs.txt", "w") as logFile:
            logFile.write("")
