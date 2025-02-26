from dataclasses import dataclass 
from typing import Dict 

@dataclass
class User:
    name: str
    last_name: str
    email: str
    username: str
    password: str
    is_active: bool = True 

    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'is_active': self.is_active
        } 

    @classmethod 
    def from_dict(cls, data: Dict) -> 'User':
        return cls(**data) 
    



