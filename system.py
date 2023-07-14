import os
import time
#from app import *

class System:
    def show_home(self):
        os.system('cls')
        print("********************************************************************************************************")
        print("*                                                                                                      *")
        print("*                                     Bienvenido a Diagenda                                            *")
        print("*                                                                                                      *")
        print("********************************************************************************************************")
        print("1. Iniciar sesión")
        print("2. Crear cuenta")
        print("")
        print("")
        print("<exit>: cerrar la aplicación")

    def show_profile(self, name, last_name):
        os.system('cls')
        print("********************************************************************************************************")
        print("*                                                                                                      *")
        print("*                                        Perfil de Usuario                                             *")
        print("*                                                                                                      *")
        print("********************************************************************************************************")
        print(f"Nombre: {name}")
        print(f"Apellidos: {last_name}")
        print("")
        print("1. Crear Evento Personal")
        print("2. Crear Grupo")
        print("3. Notificaciones")
        print("4. Eventos")
        print("5. Grupos")
        print("6. Borrar Cuenta")
        print("")
        print("<home>: volver a la vista principal")
        print("<exit>: cerrar la aplicación")

    def show_notification(self, name, last_name, notifications):
        os.system('cls')
        print("*******************************************************************************************************")
        print("*                                                                                                     *")
        print("*                                         Notificaciones                                              *")
        print("*                                                                                                     *")
        print("*******************************************************************************************************")
        print(f"Nombre: {name}")
        print(f"Apellidos: {last_name}")
        print("")
        for (notif,text) in notifications:
            print(f"{notif} {text}")
        print("")
        print("")
        print("1. Eliminar notificación <id>")
        print("")
        print("<back>: regresar al perfil")
        print("<home>: volver a la vista principal")
        print("<exit>: cerrar la aplicación")

    def show_event(self, name, last_name, events):
        os.system('cls')
        print("*******************************************************************************************************")
        print("*                                                                                                     *")
        print("*                                             Eventos                                                 *")
        print("*                                                                                                     *")
        print("*******************************************************************************************************")
        print(f"Nombre: {name}")
        print(f"Apellidos: {last_name}")
        print("")
        for (notif,text) in events:
            print(f"{notif} {text}")
        print("")
        print("")
        print("1. Eliminar evento (personal o creado) <idevent>")
        print("2. Aceptar evento (pendiente) <idevent>")
        print("3. Rechazar evento (pendiente) <idevent>")
        print("")
        print("<back>: regresar al perfil")
        print("<home>: volver a la vista principal")
        print("<exit>: cerrar la aplicación")

    def show_group(self, name, last_name, groups):
        os.system('cls')
        print("******************************************************************************************************")
        print("*                                                                                                    *")
        print("*                                             Grupos                                                 *")
        print("*                                                                                                    *")
        print("******************************************************************************************************")
        print(f"Nombre: {name}")
        print(f"Apellidos: {last_name}")
        print("")
        for (notif,text) in groups:
            print(f"{notif} {text}")
        print("")
        print("")
        print("1. Crear evento grupal <idgroup>")
        print("2. Agregar miembros (grupo creado/usuario existente) <idgroup> <iduser>")
        print("3. Solicitar miembros jerárquicamente inferior <idgroup>")
        print("")
        print("<back>: regresar al perfil")
        print("<home>: volver a la vista principal")
        print("<exit>: cerrar la aplicación")

    def show_member(self, name, last_name, creator, gname, members):
        os.system('cls')
        print("******************************************************************************************************")
        print("*                                                                                                    *")
        print("*                            Miembros Jerárquicamente Inferiores                                     *")
        print("*                                                                                                    *")
        print("******************************************************************************************************")
        print(f"Nombre: {name}")
        print(f"Apellidos: {last_name}")
        print(f"Creador: {creator}")
        print(f"Nombre de Grupo:{gname}")
        print("")
        for (notif,text) in members:
            print(f"{notif} {text}")
        print("")
        print("")
        print("1. Solicitar eventos de miembro <idmember>")
        print("")
        print("<back>: regresar al perfil")
        print("<home>: volver a la vista principal")
        print("<exit>: cerrar la aplicación")

    def start_console(self):
        while True:
            self.show_home()
            line_char = "> "
            line = input(line_char)
            if line == "2":
                os.system('cls')
                while line == "2":
                    while line == "2":
                        print("<home>: volver a la vista principal")
                        print("<exit>: cerrar la aplicación")
                        print("")
                        print("Nombre de usuario:")
                        username = input(line_char)
                        if username == "": continue
                        elif username == "exit": line = "exit"
                        elif username == "home": line = "home"
                        break
                    while line == "2":
                        print("Nombre:")
                        name = input(line_char)
                        if name == "": continue
                        elif name == "exit": line = "exit"
                        elif name == "home": line = "home"
                        break
                    while line == "2":
                        print("Apellidos:")
                        last_name = input(line_char)
                        if last_name == "": continue
                        elif last_name == "exit": line = "exit"
                        elif last_name == "home": line = "home"
                        break
                    while line == "2":
                        print("Contraseña:")
                        password = input(line_char)
                        if password == "": continue
                        elif password == "exit": line = "exit"
                        elif password == "home": line = "home"
                        break
                    while line == "2":
                        print("Repetir contraseña:")
                        password2 = input(line_char)
                        if password2 == "": continue
                        elif password2 == "exit": line = "exit"
                        elif password2 == "home": line = "home"
                        break
                    if line != "2": break
                    if password == password2:
                        print("Cuenta creada correctamente")
                        # Guardar en BD
                        line = "home"
                    else: 
                        print("No coinciden las contraseñas. Inténtelo de nuevo")
            elif line == "1":
                os.system('cls')
                while line == "1":
                    while line == "1":
                        print("<home>: volver a la vista principal")
                        print("<exit>: cerrar la aplicación")
                        print("")
                        print("Nombre de usuario:")
                        username = input(line_char)
                        if username == "": continue
                        elif username == "exit": line = "exit"
                        elif username == "home": line = "home"
                        break
                    while line == "1":
                        print("Contraseña:")
                        password = input(line_char)
                        if password == "": continue
                        elif password == "exit": line = "exit"
                        elif password == "home": line = "home"
                        break
                    if line == "1":
                        name = None
                        last_name = None
                        # CONECTO A LA BASE DE DATOS Y HALLO LA FILA QUE TIENE (SI EXISTE) <username> y <password>
                        # RECOJO DE LA INSTANCIA <name> y <last_name>
                        name = "Dianelys" # Esto lo da la BD
                        last_name = "Cruz Mengana" # Esto tambien lo da la BD
                        if name and last_name: # En realidad la condicion es que el <username> y <password> esten en la BD
                            # SE CONECTA AL SERVIDOR: lo escog o se le asigna??????
                            while True:
                                self.show_profile(name, last_name)
                                line = input(line_char)
                                if line == "1": 
                                    while True:    
                                        line = input(line_char)
                                        if line == "exit": line = "exit"
                                        if line == "home": line = "home"
                                        if line == "back": line = "back"
                                        break
                                if line == "2":
                                    while True:
                                        line = input(line_char)
                                        if line == "exit": line = "exit"
                                        if line == "home": line = "home"
                                        if line == "back": line = "back"
                                        break
                                if line == "3": 
                                    while True:
                                        notifications = None # Buscar en la BD
                                        self.show_notification(name, last_name, notifications)
                                        line = input(line_char)
                                        if line == "exit": line = "exit"
                                        if line == "home": line = "home"
                                        if line == "back": line = "back"
                                        break
                                if line == "4":
                                    while True:
                                        events = None # Buscar en la BD
                                        self.show_event(name, last_name, events)
                                        line = input(line_char)
                                        if line == "exit": line = "exit"
                                        if line == "home": line = "home"
                                        if line == "back": line = "back"
                                        break
                                if line == "5":
                                    while True:
                                        groups = None # Buscar en la BD
                                        self.show_group(name, last_name, groups)
                                        line = input(line_char)
                                        if line == "exit": line = "exit"
                                        if line == "home": line = "home"
                                        if line == "back": line = "back"
                                        break
                                if line == "6": 
                                    while True:
                                        os.system('cls')
                                        print("<back>: regresar al perfil")
                                        print("<home>: volver a la vista principal")
                                        print("<exit>: cerrar la aplicación")
                                        print("")
                                        print("¿Está seguro(a) de querer borrar su cuenta? (Y/N)")
                                        line = input(line_char)
                                        if line == "exit" or line == "home" or line == "back": break
                                        if line != "Y" and line != "N": continue
                                        if line == "Y":
                                            # Borrar de la BD este usuario
                                            line = "home"
                                            break
                                        if line == "N": break

                                if line == "exit" or line == "home": break
                        else:
                            print("Su nombre de usuario o contraseña son incorrectas. Inténtelo de nuevo")
                    if line == "exit" or line == "home": break
                if line == "exit": break 
            if line == "exit": break


sys = System().start_console()