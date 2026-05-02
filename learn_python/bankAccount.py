class BankAccount:
    transactions = []
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if (amount < 0):
            print("Negative amount cannot be deposited")
            return
        self.transactions.append("Deposited" + str(amount))
        self.balance = self.balance + amount

    def winthdraw(self, amount):
        if (amount < 0):
            print("Negative money does not exist")
            return
        self.transactions.append("Withdrawn" + str(amount))
        self.balance = self.balance - amount

    def dets(self):
        print(" ".join(self.transactions))

class SavingsAccount(BankAccount):
    def __init__(self, name, balance, savings_bal):
        super().__init__(name, balance) 
        self.savings_bal = savings_bal
    
    def __str__(self):
        return f"{self.name} account balance: {self.balance}  savings: {self.savings_bal}"
    
    def __repr__(self):
        return self.__str__()
    

def main():
    test = BankAccount("test1", 10)
    print(test)
    test.deposit(10)
    test.deposit(20)
    print(test.dets())


if __name__ == "__main__":
    main()
