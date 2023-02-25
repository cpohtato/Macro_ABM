from ..utils import *

class SellOrder():
    def __init__(self, id: int, price: float, qty: int, cost: float):
        self.id = id
        self.price = price
        self.qtySupplied = qty
        self.qtySold = 0
        self.cost = cost