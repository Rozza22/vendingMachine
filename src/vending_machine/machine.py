from .money import parse_money


class VendingMachine:
    def deposit(self, amount):
        amt = parse_money(amount)
        self.balance += amt
