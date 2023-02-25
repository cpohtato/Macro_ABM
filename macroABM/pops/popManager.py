from .pop import *

class PopManager():

    def __init__(self, initPops: int):
        
        self.listPops: list[Pop] = []
        for i in range(initPops):
            self.listPops.append(Pop(i))

    def produce(self, listProfits: list):

        decisionMap: list[list] = []
        
        for pop in self.listPops:
            decisionMap.append(pop.chooseOutput(listProfits))

        return decisionMap

    def payPopDividends(self, pop: Pop, firmManager: FirmManager):

        pop.receiveIncome(firmManager.payDividends(pop.getId())) 

    def payPopWages(self, pop: Pop, marketManager: MarketManager):

        pop.receiveIncome(marketManager.payRevenue(pop.getId(), TYPE_LABOUR)) 

    def receiveWages(self, marketManager: MarketManager, firmManager: FirmManager):

        for pop in self.listPops:
            if (pop.getOwnsFirm()): self.payPopDividends(pop, firmManager)
            else: self.payPopWages(pop, marketManager)  

    def consume(self, marketManager: MarketManager):
        
        numPops = len(self.listPops)
        randOrder = list(range(numPops))
        random.shuffle(randOrder)

        for idx in randOrder:
            self.listPops[idx].consumeGoods(marketManager)

    def settle(self):
        
        for pop in self.listPops:
            pop.settle()

    def closeOwnedFirm(self, id: int, funds: float):

        for pop in self.listPops:
            if (pop.getId() == id):
                pop.closeOwnedFirm(funds) 
                break