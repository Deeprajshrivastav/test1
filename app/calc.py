def add_two(a:int, b:int):
    return a + b 
 
def subtract(a:int, b:int):
    return a - b
def divide(a:int, b:int):
    return a / b
def product(a:int, b:int):
    return a * b


class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance
    def deposite(self, amount):
        self.balance += amount
    def withdrow(self, amount):
        self.balance -= amount
    def collect_intrest(self):
        self.balance *= 1.1