class Balance:
    def __init__(self, lent_by, lent_to, amount):
        self.lent_by = lent_by
        self.lent_to = lent_to
        self.amount = amount


class Balanaces:
    def __init__(self):
        self.balances = dict()

    def add_balance(self, lent_by, lent_to, amount):
        if lent_by not in self.balances:
            self.balances[lent_by] = {lent_to:amount}
        else:
            if lent_to not in self.balances[lent_by]:
                self.balances[lent_by][lent_to] = amount
            else:
                self.balances[lent_by][lent_to] += amount

        if lent_to not in self.balances:
            self.balances[lent_to] = {lent_by:amount*-1}
        else:
            if lent_by not in self.balances[lent_to]:
                self.balances[lent_to][lent_by] = amount * -1
            else:
                self.balances[lent_to][lent_by] -= amount
