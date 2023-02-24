from .pop import *

class PopManager():

    def __init__(self, initPops: int):
        
        self.listPops = []
        for i in range(initPops):
            self.listPops.append(Pop(i))

    def produce(self, listProfits: list):

        decisionMap: list[list] = []
        
        for pop in self.listPops:
            decisionMap.append(pop.chooseOutput(listProfits))

        return decisionMap
            

    def consume(self):
        pass

    def settle(self):
        pass