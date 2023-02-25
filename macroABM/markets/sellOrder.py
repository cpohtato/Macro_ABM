from ..utils import *

class SellOrder():

    def __init__(self, id: int, price: float, qty: int, cost: float):

        self.id = id
        self.price = price
        self.qtySupplied = qty
        self.qtySold = 0
        self.cost = cost

    def unitsAvailable(self):

        return (self.qtySupplied > self.qtySold)

    def getPrice(self):

        return self.price

    def getId(self):

        return self.id

    def makePurchase(self):

        self.qtySold += 1

    def getTotalRevenue(self):

        return self.price * self.qtySold

    def getQtySupplied(self):

        return self.qtySupplied

    def getQtySold(self):

        return self.qtySold

    def getCost(self):

        return self.cost