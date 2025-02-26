from domain.user import User 
from dataclasses import dataclass 
from typing import Dict 

@dataclass
class BankAccount: 
    user: User 
    balance: float = 0.0 
    is_active: bool = True 

    def to_dict(self) -> Dict: 
        return {
            'user': self.user.to_dict(),
            'balance': self.balance,
            'is_active': self.is_active
        } 
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BankAccount':
        return cls(user=User.from_dict(data["user"]),
                   balance=data["balance"],
                   is_active=data["is_active"]) 
    






