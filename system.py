import os

class System:
    def show_home(self):
        os.system('cls')
        print("**************************************************************")
        print("*                                                            *")
        print("*                   Bienvenido a Diagenda                    *")
        print("*                                                            *")
        print("**************************************************************")
        print("1. Iniciar sesión")
        print("2. Crear cuenta")
        print("")
        print("Para salir de la aplicación solo debe escribir <exit>")

    def show_profile(self, name, last_name):
        os.system('cls')
        print("**************************************************************")
        print("*                                                            *")
        print("*                     Perfil de Usuario                      *")
        print("*                                                            *")
        print("**************************************************************")
        print(f"Nombre: {name}")
        print(f"Apellidos: {last_name}")
        print("")
        print("1. Crear Evento Personal")
        print("2. Crear Grupo")
        print("3. Notificaciones")
        print("4. Eventos")
        print("5. Grupos")
        print("6. Borrar Cuenta")
        print("Para salir de la aplicación solo debe escribir <exit>")

    def start_console(self):
        while True:
            self.show_home()
            line_char = "> "
            while True:
                line = input(line_char)
                if line == "exit": break 
                if line == "2":
                    while True:
                        while True:
                            print("Nombre de usuario:")
                            username = input(line_char)
                            if username == "exit": line = "exit"
                            if username != "" : break
                        if line == "exit": break
                        while True:
                            print("Nombre:")
                            name = input(line_char)
                            if name == "exit": line = "exit"
                            if name != "": break
                        if line == "exit": break
                        while True:
                            print("Apellidos:")
                            last_name = input(line_char)
                            if last_name == "exit": line = "exit"
                            if last_name != "": break
                        if line == "exit": break
                        while True:
                            print("Contraseña:")
                            password = input(line_char)
                            if password != "": break
                        print("Repetir contraseña:")
                        password2 = input(line_char)
                        if password == password2:
                            # Guardar en BD
                            break
                        print("No coinciden las contraseñas. Inténtelo de nuevo")
                    if line == "2": break
                    if line == "exit": break
                if line == "1":
                    while True:
                        while True:
                            print("Nombre de usuario:")
                            username = input(line_char)
                            if username == "exit": line = "exit"
                            if username != "" : break
                        if line == "exit": break
                        while True:
                            print("Contraseña:")
                            password = input(line_char)
                            if password != "": break
                        # Conectar a BD
                        if None: #mantener la app
                            pass
                        else:
                            print("Su nombre de usuario o contraseña son  incorrectas. Inténtelo de nuevo")
                    if line == "exit": break
                else: continue
            if line == "exit": break
while True:
    sys = System().show_profile("Jordan", "Pla Gonzalez")  
    line = input()
    if line == "exit": break
sys = System().start_console()