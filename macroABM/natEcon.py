from .markets.marketManager import *
from .pops.popManager import *
from .firms.firmManager import *
import os

class NationalEconomy():

    def __init__(self, econName: str, initPops: int):

        self.econName: str = econName
        self.pops: PopManager = PopManager(initPops)
        self.markets: MarketManager = MarketManager(NUM_GOOD_TYPES)
        self.firms: FirmManager = FirmManager()

        self.listSales = np.zeros((SIM_LENGTH, NUM_GOOD_TYPES))
        self.listPrices = np.zeros((SIM_LENGTH, NUM_GOOD_TYPES))

    def simulate(self, numMonths: int):

        self.wipeLogs()

        for month in range(numMonths):
            print("Month " + str(month + 1))
            self.stepMonth()
            self.logMonth(month)

        self.displayResults()

    def stepMonth(self):
        
        self.stepProductionPhase()
        self.stepIncomePhase()
        self.stepConsumptionPhase()
        self.stepSettlementPhase()

    def stepProductionPhase(self):
        
        listProfits: list[float] = self.markets.estimateProfits()
        popDecisionMap: list[list] = self.pops.produce(listProfits)
        self.markets.makeLabourAvailable(popDecisionMap)
        self.firms.makeNewFirmsFromDecisionMap(popDecisionMap)
        self.firms.produce(self.markets)

    def stepIncomePhase(self):
        
        self.pops.receiveWages(self.markets, self.firms) 
        # self.govt.levyTax()

    def stepConsumptionPhase(self):
        
        # self.govtConsume()
        self.pops.consume(self.markets)

    def stepSettlementPhase(self):

        self.pops.settle()
        self.firms.settle(self.markets)
        self.markets.settle()
        self.firms.closeUnprofitableFirms(self.pops) 

    def logMonth(self, month: int):
        
        sales, avgPrices = self.markets.logMonth(month, self.econName)
        numFirms, listProfits = self.firms.logMonth(month, self.econName)

        self.listSales[month] = sales
        self.listPrices[month] = avgPrices

    def displayResults(self):

        arrTime = list(range(1, SIM_LENGTH + 1))
        
        plt.figure(1)
        plt.plot(arrTime, self.listPrices[:SIM_LENGTH, TYPE_LABOUR], label=DICT_GOOD_TYPES[TYPE_LABOUR])
        plt.plot(arrTime, self.listPrices[:SIM_LENGTH, TYPE_PRODUCE], label=DICT_GOOD_TYPES[TYPE_PRODUCE])
        plt.plot(arrTime, self.listPrices[:SIM_LENGTH, TYPE_SERVICES], label=DICT_GOOD_TYPES[TYPE_SERVICES])
        plt.title("Market Prices")
        plt.xlabel("Month")
        plt.ylabel("Price")
        plt.xlim(1, SIM_LENGTH)
        plt.legend()

        plt.figure(2)
        plt.plot(arrTime, self.listSales[:SIM_LENGTH, TYPE_LABOUR], label=DICT_GOOD_TYPES[TYPE_LABOUR])
        plt.plot(arrTime, self.listSales[:SIM_LENGTH, TYPE_PRODUCE], label=DICT_GOOD_TYPES[TYPE_PRODUCE])
        plt.plot(arrTime, self.listSales[:SIM_LENGTH, TYPE_SERVICES], label=DICT_GOOD_TYPES[TYPE_SERVICES])
        plt.title("Market Sales")
        plt.xlabel("Month")
        plt.ylabel("Sales")
        plt.xlim(1, SIM_LENGTH)
        plt.legend()

        plt.show()

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
