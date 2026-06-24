from .money import parse_money


class VendingMachine:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        amt = parse_money(amount)
        self.balance += amt
