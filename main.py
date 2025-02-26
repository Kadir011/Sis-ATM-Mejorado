from infrastructure.storage import JsonStorage
from services.atm_service import ATMService
from ui.console_interface import ConsoleInterface 

def main():
    storage = JsonStorage()
    atm_service = ATMService(storage)
    interface = ConsoleInterface(atm_service)
    
    if interface.show_login_menu():
        interface.show_main_menu() 


if __name__ == '__main__':
   main() 




