class BankAccount:
    def __init__(self, account_number, holder_name, balance=0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance

    def display_info(self):
        return f"{self.account_number} - {self.holder_name}: ₹{self.balance}"

class SavingsAccount(BankAccount):
    def __init__(self, account_number, holder_name, balance=0, interest_rate=0.03):
        super().__init__(account_number, holder_name, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        self.balance += self.balance * self.interest_rate

class CurrentAccount(BankAccount):
    def __init__(self, account_number, holder_name, balance=0, overdraft_limit=5000):
        super().__init__(account_number, holder_name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if self.balance + self.overdraft_limit >= amount:
            self.balance -= amount
            return True
        return False

import pickle
import os

class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.data_file = f"{self.name.replace(' ', '_')}_data.pkl"
        self.load_accounts()

    def create_account(self, acc_type, acc_no, holder_name, password):
        if acc_no in self.accounts:
            return False
        if acc_type == "Savings":
            self.accounts[acc_no] = SavingsAccount(acc_no, holder_name, password)
        elif acc_type == "Current":
            self.accounts[acc_no] = CurrentAccount(acc_no, holder_name, password)
        self.save_accounts()
        return True

    def get_account(self, acc_no):
        return self.accounts.get(acc_no)

    def save_accounts(self):
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.accounts, f)

    def load_accounts(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                self.accounts = pickle.load(f)
