import random 
import string 

class PasswordGenerator:
    def generate(self, length: int = 16) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length)) 
    

