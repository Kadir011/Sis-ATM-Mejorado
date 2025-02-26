import os
import json 
from typing import List
from domain.user import User 
from domain.account import BankAccount 

class JsonStorage:
    def __init__(self, filename: str = "json/atm.json"):
        self.filename = filename

    def save(self, users: List[User], accounts: List[BankAccount]) -> None:
        try:
            data = {
                "users": [user.to_dict() for user in users],
                "accounts": [account.to_dict() for account in accounts]
            }
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            raise Exception(f"Error saving data: {e}")

    def load(self) -> tuple[List[User], List[BankAccount]]:
        try:
            if not os.path.exists(self.filename):
                return [], []
            
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                users = [User.from_dict(user) for user in data.get("users", [])]
                accounts = [BankAccount.from_dict(account) for account in data.get("accounts", [])]
                return users, accounts
        except Exception as e:
            raise Exception(f"Error loading data: {e}")






