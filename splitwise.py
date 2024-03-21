import time
import pandas as pd

from expenses import Expense
from balances import Balanaces

from id_generator import IDGenerator
from user import User


class Splitwise:

    def __init__(self):
        self.users = pd.DataFrame(columns=['user_id', 'name', 'email', 'phone_number'])
        self.users.set_index('user_id', inplace=True)

        self.expenses = pd.DataFrame(
            columns=['payer', 'datetime', 'expense_type', 'amount_paid', 'users_involved', 'shares'])

        self.balances = pd.DataFrame(columns=['lent_by', 'lent_to', 'amount'])
        # self.balances.set_index(['lent_by', 'lent_to'],inplace=True)

    def add_user(self, user_id):
        if not self.user_exists(user_id):
            user = User(user_id)
            self.users.loc[user_id] = user.__dict__

    def user_exists(self, user_id):
        return user_id not in self.users.index

    def show(self, user_id):
        if user_id and self.user_exists(user_id) and not self.balances.empty:
            lent_to_other = self.balances[(self.balances['lent_by'] == user_id) & (self.balances['amount'] > 0)]
            if not lent_to_other.empty:
                for index, row in lent_to_other.iterrows():
                    lent_by,lent_to,amout = row['lent_by'],row['lent_to'],row['amount']
                    print(f'{lent_to} owes {user_id}: {amout}')

            lent_from_other = self.balances[(self.balances['lent_by'] == user_id) & (self.balances['amount'] < 0)]
            if not lent_from_other.empty:
                for index, row in lent_from_other.iterrows():
                    lent_by,lent_to,amount = row['lent_by'],row['lent_to'],row['amount']
                    print(f'{user_id} owes {lent_to}: {amount * -1}')

        elif not user_id and not self.balances.empty:
            lent_to_other = self.balances[self.balances['amount'] > 0]
            if not lent_to_other.empty:
                for index, row in lent_to_other.iterrows():
                    lent_by,lent_to,amount = row['lent_by'],row['lent_to'],row['amount']
                    print(f'{lent_to} owes {lent_by}: {amount}')

        else:
            print('No expenses')


    def add_expense(self, expense_type, payer, amount_paid, users_involved, shares=[]):
        self.add_user(payer)
        for user in users_involved:
            self.add_user(user)

        new_expense = Expense(payer, expense_type, amount_paid, users_involved, shares)
        self.expenses.loc[len(self.expenses)] = new_expense.__dict__
        splits = new_expense.split_expense()
        for expense in splits:
            lent_to, amount_lent = expense[0], expense[1]
            lent_by = new_expense.payer.user_id
            self.add_balance(lent_by, lent_to, amount_lent)

    def add_balance(self, lent_by, lent_to, amount_lent):
        balances = self.balances[(self.balances['lent_by'] == lent_by) & (self.balances['lent_to'] == lent_to)]
        if balances.empty:
            self.balances.loc[len(self.balances)] = [lent_by, lent_to, amount_lent]
        else:
            index = balances.index[0]  # Get the index of the first matching row
            self.balances.loc[index, 'amount'] += amount_lent

        balances = self.balances[(self.balances['lent_by'] == lent_to) & (self.balances['lent_to'] == lent_by)]
        if balances.empty:
            self.balances.loc[len(self.balances)] = [lent_to, lent_by, amount_lent * -1]
        else:
            index = balances.index[0]  # Get the index of the first matching row
            self.balances.loc[index, 'amount'] -= amount_lent