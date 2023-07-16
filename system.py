import os
from app import *

# TASKS (MIOS NO LOS BORRES PLIS):
# MOSTRAR ASIGNACION DE ROL Y LEVEL PARA ANNADIR MIEMBROS SI ES JERARQUICO
# ELIMINAR EVENTOS COMPROBANDO CREADOR OR PERSONAL
# DECLINAR EVENTOS COMPROBANDO QUE ESTAN EN PENDIENTES
# CREAR CUENTA CON USUARIO UNICO SI NO, NOTIFCARLO

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
        #print("6. Borrar Cuenta")
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
        user = Client()
        while True:
            self.show_home()
            line_char = "> "
            line = input(line_char)
            if line == "2":
                while line == "2":
                    os.system('cls')
                    print("<home>: volver a la vista principal")
                    print("<exit>: cerrar la aplicación")
                    print("")
                    while line == "2":
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
                        user.create_account(username,name,last_name,password)
                        print("Cuenta creada correctamente")
                        time.sleep(2)
                        line = "home"
                    else: 
                        print("No coinciden las contraseñas. Inténtelo de nuevo")
                        time.sleep(2)
            elif line == "1":
                while line == "1":
                    os.system('cls')
                    print("<home>: volver a la vista principal")
                    print("<exit>: cerrar la aplicación")
                    print("")
                    while line == "1":
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
                        name, last_name = user.get_account(username, password)
                        name = "Diane"
                        last_name = "Cruz Mengana"
                        # CONECTO A LA BASE DE DATOS Y HALLO LA FILA QUE TIENE (SI EXISTE) <username> y <password>
                        # RECOJO DE LA INSTANCIA <name> y <last_name>
                        if name and last_name: # En realidad la condicion es que el <username> y <password> esten en la BD
                            # SE CONECTA AL SERVIDOR: lo escog o se le asigna??????
                            while True:
                                self.show_profile(name, last_name)
                                line = input(line_char)
                                if line == "1": 
                                    while line == "1":
                                        os.system('cls')
                                        print("<back>: regresar al perfil")
                                        print("<home>: volver a la vista principal")
                                        print("<exit>: cerrar la aplicación")
                                        print("")
                                        while line == "1":
                                            print("Nombre de evento:")
                                            ename = input(line_char)
                                            if ename == "": continue
                                            elif ename == "exit": line = "exit"
                                            elif ename == "home": line = "home"
                                            elif ename == "back": line = "back"
                                            break
                                        while line == "1":
                                            print("Fecha inicial:")
                                            print("formato: <Y-M-D HH:MM> - 24 Horas")
                                            date_ini = input(line_char)
                                            if date_ini == "": continue
                                            elif date_ini == "exit": line = "exit"
                                            elif date_ini == "home": line = "home"
                                            elif date_ini == "back": line = "back"
                                            break
                                        while line == "1":
                                            print("Fecha final:")
                                            print("formato: <Y/M/D-HH:MM> - 24 Horas")
                                            date_end = input(line_char)
                                            if date_end == "": continue
                                            elif date_end == "exit": line = "exit"
                                            elif date_end == "home": line = "home"
                                            elif date_end == "back": line = "back"
                                            break
                                        if line != "1": break
                                        if date_end < date_ini: 
                                            print("Las fechas proporcionadas son incorrectas. Inténtelo de nuevo")
                                            time.sleep(2)
                                            continue
                                        while line == "1":
                                            print("Privacidad:")
                                            print("1. Privado")
                                            print("2. Público")
                                            privacity = input(line_char)
                                            if privacity == "": continue
                                            elif privacity == "exit": line = "exit"
                                            elif privacity == "home": line = "home"
                                            elif privacity == "back": line = "back"
                                            elif privacity == "1": privacity = Privacity.Private.value
                                            elif privacity == "2": privacity = Privacity.Public.value
                                            else: continue
                                            break
                                        if line != "1": break
                                        user.create_personal_event(ename, date_ini, date_end, privacity)
                                        print("Evento personal creado correctamente")
                                        time.sleep(2)
                                        break
                                if line == "2":
                                    # print("2. Crear Grupo")
                                    while True:
                                        line = input(line_char)
                                        if line == "exit": line = "exit"
                                        if line == "home": line = "home"
                                        if line == "back": line = "back"
                                        break
                                if line == "3": 
                                    # print("3. Notificaciones")
                                    while True:
                                        notifications = None # Buscar en la BD
                                        self.show_notification(name, last_name, notifications)
                                        line = input(line_char)
                                        if line == "exit": line = "exit"
                                        if line == "home": line = "home"
                                        if line == "back": line = "back"
                                        break
                                if line == "4":
                                    # print("4. Eventos")
                                    while True:
                                        events = None # Buscar en la BD
                                        self.show_event(name, last_name, events)
                                        line = input(line_char)
                                        if line == "exit": line = "exit"
                                        if line == "home": line = "home"
                                        if line == "back": line = "back"
                                        break
                                if line == "5":
                                    # print("5. Grupos")
                                    while True:
                                        groups = None # Buscar en la BD
                                        self.show_group(name, last_name, groups)
                                        line = input(line_char)
                                        if line == "exit": line = "exit"
                                        if line == "home": line = "home"
                                        if line == "back": line = "back"
                                        break
                                # if line == "6": 
                                #     while True:
                                #         os.system('cls')
                                #         print("<back>: regresar al perfil")
                                #         print("<home>: volver a la vista principal")
                                #         print("<exit>: cerrar la aplicación")
                                #         print("")
                                #         print("¿Está seguro(a) de querer borrar su cuenta? (Y/N)")
                                #         line = input(line_char)
                                #         if line == "exit" or line == "home" or line == "back": break
                                #         if line != "Y" and line != "N": continue
                                #         if line == "Y":
                                #             user.delete_account()
                                #             line = "home"
                                #             break
                                #         if line == "N": break
                                if line == "exit" or line == "home": break
                        else:
                            print("Su nombre de usuario o contraseña son incorrectas. Inténtelo de nuevo")
                            time.sleep(2)
                    if line == "exit" or line == "home": break
                if line == "exit": break 
            if line == "exit": break


sys = System().start_console()