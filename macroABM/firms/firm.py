from ..utils import *

class Firm():

    def __init__(self, firmId: int, ownerId: int, goodType: int, initInvestment: float):
        
        self.firmId = firmId
        self.ownerId = ownerId
        self.goodType = goodType
        self.funds = initInvestment

    def getFirmId(self):
        
        return self.firmId