# Task 06 – Banking Ledger with OOP

class Account:

    def __init__(self, balance):
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):

        if amount <= 0:
            print("Invalid amount")
            return

        self.balance += amount
        self.transactions.append("Deposit: " + str(amount))

    def withdraw(self, amount):

        if amount <= 0:
            print("Invalid amount")

        elif amount > self.balance:
            print("Insufficient balance")

        else:
            self.balance -= amount
            self.transactions.append("Withdraw: " + str(amount))


class Bank:

    def __init__(self):
        self.accounts = {}

    def create_account(self, account_id, balance):
        self.accounts[account_id] = Account(balance)

    def transfer(self, sender, receiver, amount):

        if sender not in self.accounts or receiver not in self.accounts:
            print("Account not found")
            return

        if amount <= 0:
            print("Invalid amount")
            return

        if self.accounts[sender].balance < amount:
            print("Insufficient balance")
            return

        self.accounts[sender].balance -= amount
        self.accounts[receiver].balance += amount

        print("Transfer successful")


bank = Bank()

bank.create_account("A", 1000)
bank.create_account("B", 200)

bank.transfer("A", "B", 350)

print("A Balance:", bank.accounts["A"].balance)
print("B Balance:", bank.accounts["B"].balance)
