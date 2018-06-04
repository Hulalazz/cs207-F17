from enum import Enum
class AccountType(Enum):
    SAVINGS = 1
    CHECKING = 2

class BankAccount:
    def __init__(self, owner, accountType):
        self.owner = owner
        self.accountType = accountType
        self.balance = 0
        
    def withdraw(self, amount):
        if self.balance >= amount and amount >= 0:
            self.balance -= amount
            return True
        else:
            return False
        
    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            return True
        else:
            return False
        
    def __str__(self):
        return self.owner + "'s " + self.accountType.name + " Account"
    
    def __len__(self):
        return self.balance

class BankUser:
    def __init__(self, owner):
        self.owner = owner
        self.accounts = {}
        
    def addAccount(self, accountType):
        if accountType.name in self.accounts:
            return False
        else:
            self.accounts[accountType.name] = BankAccount(self.owner, accountType)
            return True
        
    def getBalance(self, accountType):
        return len(self.accounts[accountType.name]) if accountType.name in self.accounts else -1
        
    def deposit(self, accountType, amount):
        if accountType.name in self.accounts:
            return self.accounts[accountType.name].deposit(amount)
        else:
            return False
        
    def withdraw(self, accountType, amount):
        if accountType.name in self.accounts:
            return self.accounts[accountType.name].withdraw(amount)
        else:
            return False
        
    def __str__(self):
        s = self.owner + "'s Accounts:\n"
        for t, a in self.accounts.items():
            s += t + ": " + str(len(a)) + "\n"
        return s

def ATMSession(bankUser):
    def Interface():
        option = 0
        while option != 1:
            try:
                option = int(input('Enter Option:\n1)Exit\n2)Create Account\n3)Check Balance\n4)Deposit\n5)WithDraw\n\n'))
                if option > 1:
                    accountOption = 0
                    while accountOption != 1 and accountOption != 2:
                        accountOption = int(input('Select Account Type:\n1) Checking\n2) Savings\n'))
                        if accountOption != 1 and accountOption != 2:
                            print('Invalid Account Specified\n')
                    accountType = AccountType.SAVINGS if accountOption == 2 else AccountType.CHECKING
                    if option == 2:
                        if bankUser.addAccount(accountType):
                            print('Account Created\n')
                        else:
                            print('Account Already Exists\n')
                    elif option == 3:
                        balance = bankUser.getBalance(accountType)
                        if balance < 0:
                            print('Account Not Found\n')
                        else:
                            print('Balance:{}'.format(balance))
                    else:
                        amount = -1
                        while amount < 0:
                            amount = int(input('Enter integer amount, cannot be negative\n'))
                            if amount < 0:
                                print('Invalid Amount Entered\n')
                        bankFunc = bankUser.deposit if option == 4 else bankUser.withdraw
                        if bankFunc(accountType, amount):
                            print('Transaction was successful\n')
                        else:
                            balance = bankUser.getBalance(accountType)
                            if balance >= 0:
                                print('Insufficient Funds\n')
                            else:
                                print('No Account Found\n')
                            
                print(str(bankUser))
            except ValueError:
                print('Invalid Entry')
                option=1
    return Interface    
