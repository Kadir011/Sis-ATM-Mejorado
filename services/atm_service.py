from typing import List, Optional
from domain.user import User
from domain.account import BankAccount
from infrastructure.storage import JsonStorage
from services.password_generate import PasswordGenerator 

class ATMService: 
    def __init__(self, storage: JsonStorage):
        self.storage = storage
        self.users: List[User] = []
        self.accounts: List[BankAccount] = []
        self.current_account: Optional[BankAccount] = None
        self.password_generator = PasswordGenerator()
        self.load_data() 

    def load_data(self) -> None:
        self.users, self.accounts = self.storage.load()

    def save_data(self) -> None:
        self.storage.save(self.users, self.accounts) 

    def register_user(self, name: str, last_name: str, email: str, username: str, password: str) -> bool:
        new_user = User(name, last_name, email, username, password)
        new_account = BankAccount(new_user)
        self.users.append(new_user)
        self.accounts.append(new_account)
        self.save_data()
        return True 
    
    def login_user(self, username: str, password: str) -> bool:
        for account in self.accounts:
            if account.user.username == username and account.user.password == password:
                self.current_account = account
                return True
        return False 
    
    def deposit(self, amount: float) -> Optional[float]:
        if self.current_account and amount > 0:
            self.current_account.balance += amount 
            self.save_data()
            return self.current_account.balance 
        return None 
    
    def withdraw(self, amount: float) -> Optional[float]:
        if self.current_account and amount > 0 and self.current_account.balance >= amount:
            self.current_account.balance -= amount 
            self.save_data()
            return self.current_account.balance 
        return None 
    
    def get_balance(self) -> Optional[float]:
        return self.current_account.balance if self.current_account else None 
    
    def change_password(self, new_password: str) -> bool:
        if self.current_account:
            self.current_account.user.password = new_password
            self.save_data()
            return True
        return False

    def get_current_user(self) -> Optional[User]:
        return self.current_account.user if self.current_account else None 

    def toggle_user_status(self) -> bool:
        if self.current_account:
            self.current_account.user.is_active = not self.current_account.user.is_active
            self.save_data()
            return True
        return False

    def toggle_account_status(self) -> bool:
        if self.current_account:
            self.current_account.is_active = not self.current_account.is_active
            self.save_data()
            return True
        return False 
    






