import time

from user import User

from id_generator import IDGenerator


class Expense:
    def __init__(self, payer, expense_type, amount_paid, users_involved, shares):
        self.expense_id = IDGenerator.generate_unique_id()
        self.payer = User(payer)
        self.datetime = time.time()
        self.expense_type = expense_type
        self.amount_paid = amount_paid
        self.users_involved = users_involved
        self.shares = shares

    def split_expense(self):
        '''
        User , Share, Unit(Percentage/Exact/Equal)
        :return:
        '''

        expenses = []
        if self.expense_type == 'EQUAL':
            each_share = round(self.amount_paid / len(self.users_involved), 2)
            # handle decimal values laters
            expenses += [(user, each_share, each_share) for user in self.users_involved if user != self.payer.user_id]
            rounded_total = round(each_share + self.amount_paid - (each_share * len(self.users_involved)), 2)
            expenses.append((self.payer.user_id, rounded_total, each_share))


        elif self.expense_type == 'EXACT':
            if sum(self.shares) != self.amount_paid:
                raise Exception('Sum of all exact shares is not equal to paid amount')
            others_expenses = 0
            for user, share in zip(self.users_involved, self.shares):
                expenses.append((user, share, share))
                others_expenses += share
            expenses.append(
                (self.payer.user_id, self.amount_paid - others_expenses, self.amount_paid - others_expenses))

        elif self.expense_type == 'PERCENT':
            if sum(self.shares) != 100:
                raise Exception('Sum of all percentages is not equal to 100')
            expenses += [(user, (self.amount_paid * share) / 100, share) for user, share in
                         zip(self.users_involved, self.shares)]
        return expenses