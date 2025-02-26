import time 
from services.atm_service import ATMService
from services.password_generate import PasswordGenerator 

class ConsoleInterface:
    def __init__(self, atm_service: ATMService):
        self.atm = atm_service 
        self.password_generator = PasswordGenerator() 

    def get_user_input(self, prompt: str) -> str:
        return input(prompt).strip()

    def show_login_menu(self) -> bool:
        while True:
            print("\n=== Bienvenido al sistema ATM ===")
            print("1. Iniciar sesión")
            print("2. Registro de usuario")
            print("3. Salir")
            
            option = self.get_user_input("Seleccione una opción: ") 

            match option:
                case '1':
                    if self.handle_login():
                        return True 
                case '2':
                    self.handle_register()
                case '3':
                    print("Adiós")
                    return False 
                case _:
                    print("Opción no válida")
                    time.sleep(5) 

    def handle_login(self) -> bool:
        attempts = 3 

        while attempts > 0:
            username = self.get_user_input("Nombre de usuario: ")
            password = self.get_user_input("Contraseña: ") 

            if self.atm.login_user(username, password):
               print(f"Bienvenido {self.atm.get_current_user().name}")
               return True 
            
            attempts -= 1 
            print(f"Credenciales incorrectas. Intentos restantes: {attempts}") 
        
        print("Máximo de intentos alcanzado")
        return False 
    
    def handle_register(self) -> bool:
        name = self.get_user_input("Nombre: ")
        last_name = self.get_user_input("Apellido: ")
        email = self.get_user_input("Email: ")
        username = self.get_user_input("Nombre de usuario: ") 

        if self.get_user_input("¿Generar contraseña automática? (si/no): ").lower() == "si":
           password = self.password_generator.generate() 
           print(f"Contraseña generada: {password}") 
           if self.get_user_input("¿Aceptar esta contraseña? (si/no): ").lower() != "si":
               password = self.get_manual_password() 

        password = self.get_manual_password() 

        if self.atm.register_user(name, last_name, email, username, password):
            print("Usuario registrado correctamente") 

    def get_manual_password(self) -> str:
        while True:
            password = self.get_user_input("Contraseña: ")
            confirm = self.get_user_input("Confirme contraseña: ") 

            if password != confirm:
                print("Las contraseñas no coinciden")
                continue 
            
            return password 
        
    def show_main_menu(self) -> bool:
        while True:
            print("\n=== Menú Principal ===")
            print("1. Depositar")
            print("2. Retirar")
            print("3. Consultar saldo")
            print("4. Consultar datos")
            print("5. Cambiar contraseña")
            print("6. Cambiar estado del usuario")
            print("7. Cambiar estado de la cuenta")
            print("8. Salir")
            
            option = self.get_user_input("Seleccione una opción: ") 

            match option:
                case '1':
                    self.handle_deposit() 
                case '2':
                    self.handle_withdraw()
                case '3':
                    self.handle_balance()
                case '4':
                    self.handle_user_info()
                case '5':
                    self.handle_password_change() 
                case '6':
                    self.handle_user_status_change()
                case '7':
                    self.handle_account_status_change()
                case '8':
                    print(f"Adiós {self.atm.get_current_user().name}")
                    break
                case _:
                    print("Opción no válida")
                    time.sleep(5) 

    def handle_deposit(self) -> None:
        try:
            amount = float(self.get_user_input("Cantidad a depositar: ")) 

            if balance := self.atm.deposit(amount):
                print(f"Depósito exitoso. Saldo actual: {balance:.2f}")
            else:
                print("Error al depositar")
        except ValueError:
            print("Cantidad inválida") 

    def handle_withdraw(self) -> None:
        try:
            amount = float(self.get_user_input("Cantidad a retirar: "))

            if balance := self.atm.withdraw(amount):
                print(f"Retiro exitoso. Saldo actual: {balance:.2f}")
            else:
                print("Error al retirar")
        except ValueError:
            print("Cantidad inválida") 

    def handle_balance(self) -> None:
        if balance := self.atm.get_balance():
            print(f"Saldo actual: {balance:.2f}")
        else:
            print("No hay cuenta activa") 

    def handle_user_info(self) -> None:
        if user := self.atm.get_current_user():
            print(f"Nombre: {user.name}")
            print(f"Apellido: {user.last_name}")
            print(f"Email: {user.email}")
            print(f"Usuario: {user.username}")
            print(f"Estado: {'Activo' if user.is_active else 'Inactivo'}")
            print(f"Saldo: {self.atm.get_balance():.2f}") 
        else:
            print("No hay cuenta activa") 
    
    def handle_password_change(self) -> None:
        if self.get_user_input("¿Generar contraseña automática? (si/no): ").lower() == "si":
            new_password = self.password_generator.generate()
            print(f"Contraseña generada: {new_password}")
            if self.get_user_input("¿Aceptar esta contraseña? (si/no): ").lower() != "si":
                new_password = self.get_manual_password() 

        new_password = self.get_manual_password() 

        if self.atm.change_password(new_password):
            print("Contraseña cambiada correctamente") 
    
    def handle_user_status_change(self) -> None:
        if user := self.atm.get_current_user():
            current_status = "Activo" if user.is_active else "Inactivo"
            print(f"Estado actual del usuario: {current_status}")
            if self.get_user_input("¿Cambiar estado? (si/no): ").lower() == "si":
                if not self.atm.toggle_user_status():
                   print("Error al cambiar el estado del usuario") 

                new_status = "Activo" if user.is_active else "Inactivo"
                print(f"Estado del usuario cambiado a: {new_status}")
            else:
                print("Cambio de estado cancelado")
        else:
            print("No hay usuario activo")

    def handle_account_status_change(self) -> None:
        if self.atm.current_account:
            current_status = "Activo" if self.atm.current_account.is_active else "Inactivo"
            print(f"Estado actual de la cuenta: {current_status}")
            if self.get_user_input("¿Cambiar estado? (si/no): ").lower() == "si":
                if not self.atm.toggle_account_status():
                   print("Error al cambiar el estado de la cuenta") 
                
                new_status = "Activo" if self.atm.current_account.is_active else "Inactivo"
                print(f"Estado de la cuenta cambiado a: {new_status}")
            else:
                print("Cambio de estado cancelado")
        else:
            print("No hay cuenta activa")




