import os
import platform
from client import *

class System:
    operative_system = platform.system()
    def console_cleaned(self):
        if self.operative_system == 'Windows': os.system('cls')
        elif self.operative_system == 'Linux': os.system('clear')
        else: os.system('clear')

    def show_home(self):
        self.console_cleaned()
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
        self.console_cleaned()
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
        print("")
        print("<home>: volver a la vista principal")
        print("<exit>: cerrar la aplicación")

    def show_notification(self, name, last_name, ids, texts):
        self.console_cleaned()
        print("*******************************************************************************************************")
        print("*                                                                                                     *")
        print("*                                         Notificaciones                                              *")
        print("*                                                                                                     *")
        print("*******************************************************************************************************")
        print(f"Nombre: {name}")
        print(f"Apellidos: {last_name}")
        print("")
        for i,text in enumerate(texts):
            print(f"{ids[i]} {text}")
        print("")
        print("<back>: regresar al perfil")
        print("<home>: volver a la vista principal")
        print("<exit>: cerrar la aplicación")
        print("")
        print("1. Eliminar notificación <id>")
        print("")

    def show_event(self, userkey, name, last_name, ids_event, event_names, dates_ini, dates_end, states , visibilities, creators, member=None):
        self.console_cleaned()
        print("*******************************************************************************************************")
        print("*                                                                                                     *")
        if member is None: print("*                                             Eventos                                                 *")
        else: print("*                                        Eventos de Miembro                                           *")
        print("*                                                                                                     *")
        print("*******************************************************************************************************")
        if member is None:
            print(f"Nombre: {name}")
            print(f"Apellidos: {last_name}")
            print("")
            for i,ename in enumerate(event_names):
                if str(creators[i]) == str(userkey): print(f"{ids_event[i]} {ename} {dates_ini[i]} {dates_end[i]} {states[i]} {visibilities[i]} Creador")
                else: print(f"{ids_event[i]} {ename} {dates_ini[i]} {dates_end[i]} {states[i]} {visibilities[i]} No creador")
        else:
            print(f"Miembro ID: {member}")
            print("")
            for i,ename in enumerate(event_names):
                print(f"{ename} {dates_ini[i]} {dates_end[i]} {states[i]}")     
        print("")
        print("<back>: regresar al perfil")
        print("<home>: volver a la vista principal")
        print("<exit>: cerrar la aplicación")
        if member is None:
            print("")
            print("1. Eliminar evento (personal o creado) <idevent>")
            print("2. Aceptar evento (pendiente) <idevent>")
            print("3. Rechazar evento (pendiente) <idevent>")
            print("")

    def show_group(self, name, last_name, ids_group, group_names, group_types, group_refs, userkey):
        self.console_cleaned()
        print("******************************************************************************************************")
        print("*                                                                                                    *")
        print("*                                             Grupos                                                 *")
        print("*                                                                                                    *")
        print("******************************************************************************************************")
        print(f"Nombre: {name}")
        print(f"Apellidos: {last_name}")
        print("")
        for i,ids in enumerate(ids_group):
            if userkey == group_refs[i]: print(f"{ids} {group_names[i]} {group_types[i]} Creador")
            else: print(f"{ids} {group_names[i]} {group_types[i]} No creador")
        print("")
        print("<back>: regresar al perfil")
        print("<home>: volver a la vista principal")
        print("<exit>: cerrar la aplicación")
        print("")
        print("1. Crear evento grupal <idgroup>")
        print("2. Agregar miembros (grupo creado/usuario existente) <idgroup>")
        print("3. Solicitar miembros jerárquicamente inferior <idgroup>")
        print("")

    def show_member(self, name, last_name, creator, gname, members):
        self.console_cleaned()
        print("******************************************************************************************************")
        print("*                                                                                                    *")
        print("*                            Miembros Jerárquicamente Inferiores                                     *")
        print("*                                                                                                    *")
        print("******************************************************************************************************")
        print(f"Nombre: {name}")
        print(f"Apellidos: {last_name}")
        print(f"Creador ID: {creator}")
        print(f"Nombre de Grupo: {gname}")
        print("")
        for id_member in members:
            print(f"{id_member}")
        print("")
        print("<back>: regresar al perfil")
        print("<home>: volver a la vista principal")
        print("<exit>: cerrar la aplicación")
        print("")
        print("1. Solicitar eventos de miembro (respetando su privacidad) <idmember>")
        print("")

    def start_console(self):
        user = Client(("127.0.0.1",5557),("127.0.0.1",int("5030")))
        while True:
            self.show_home()
            line_char = "> "
            line = input(line_char)
            if line == "2":
                while line == "2":
                    self.console_cleaned()
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
                        boolean = user.create_account(username,name,last_name,password)
                        time.sleep(2)
                        line = "home"
                        if boolean == False:
                            print("Nombre de usuario existente")
                            time.sleep(2) 
                    else: 
                        print("No coinciden las contraseñas. Inténtelo de nuevo")
                        time.sleep(2)
            elif line == "1":
                while line == "1":
                    self.console_cleaned()
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
                        if name and last_name:
                            while True:
                                self.show_profile(name, last_name)
                                line = input(line_char)
                                if line == "1": 
                                    while line == "1":
                                        self.console_cleaned()
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
                                            print("formato: <Y-M-D HH:MM> - 24 Horas")
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
                                        user.create_personal_event(user.user_key,ename,date_ini,date_end,privacity)
                                        time.sleep(2)
                                        break
                                if line == "2":   
                                    while line == "2":
                                        self.console_cleaned()
                                        print("<back>: regresar al perfil")
                                        print("<home>: volver a la vista principal")
                                        print("<exit>: cerrar la aplicación")
                                        print("")
                                        while line == "2":
                                            print("Nombre de grupo:")
                                            gname = input(line_char)
                                            if gname == "": continue
                                            elif gname == "exit": line = "exit"
                                            elif gname == "home": line = "home"
                                            elif gname == "back": line = "back"
                                            break 
                                        while line == "2":
                                            print("Tipo de grupo:")
                                            print("1. Jerárquico")
                                            print("2. No Jerárquico")
                                            gtype = input(line_char)
                                            if gtype == "": continue
                                            elif gtype == "exit": line = "exit"
                                            elif gtype == "home": line = "home"
                                            elif gtype == "back": line = "back"
                                            elif gtype == "1": gtype = GType.Hierarchical.value
                                            elif gtype == "2": gtype = GType.Non_hierarchical.value
                                            else: continue
                                            break
                                        if line != "2": break
                                        user.create_group(gname, gtype)
                                        time.sleep(2)
                                        break
                                if line == "3": 
                                    ids,texts = user.get_notifications()
                                    while True:
                                        self.show_notification(name, last_name, ids, texts)
                                        line = input(line_char)
                                        lines = line.split(" ",1)
                                        line = lines[0]
                                        idnotif = lines[1] if len(lines) > 1 else None
                                        if line == "1" and idnotif:
                                            idn = None
                                            try: idn = int(idnotif)
                                            except: continue
                                            if idn and idn in ids: 
                                                user.delete_notification(idn)
                                                time.sleep(2)
                                                break
                                        if line == "exit" or line == "home" or line == "back": break
                                if line == "4":
                                    ids_event,event_names,dates_ini,dates_end,states,visibilities,creators,id_groups,sizes=user.get_all_events()
                                    while True:
                                        self.show_event(user.user_key,name,last_name,ids_event,event_names,dates_ini,dates_end,states,visibilities,creators)
                                        line = input(line_char)
                                        lines = line.split(" ",1)
                                        line = lines[0]
                                        idevent = lines[1] if len(lines) > 1 else None
                                        if line == "1" and idevent:
                                            if idevent in ids_event:
                                                index = ids_event.index(idevent)
                                                if states[index] == State.Personal.value or creators[index] == str(user.user_key):
                                                    user.delete_event(idevent)
                                                    time.sleep(2)
                                                    break
                                                else: 
                                                    print("Este evento no es personal o no es creado por usted")
                                                    time.sleep(2)
                                        elif line == "2" and idevent:
                                            if idevent in ids_event:
                                                index = ids_event.index(idevent)
                                                if states[index] == State.Pendient.value:
                                                    user.accept_pendient_event(idevent)
                                                    time.sleep(2)
                                                    break
                                                else: 
                                                    print("Este evento no está pendiente a confirmación")
                                                    time.sleep(2)
                                        elif line == "3" and idevent:
                                            if idevent in ids_event:
                                                    index = ids_event.index(idevent)
                                                    if states[index] == State.Pendient.value:
                                                        user.decline_pendient_event(idevent)
                                                        time.sleep(2)
                                                        break
                                                    else: 
                                                        print("Este evento no está pendiente a confirmación")
                                                        time.sleep(2)
                                        if line == "exit" or line == "home" or line == "back": break
                                if line == "5":
                                    ids_group,group_names,group_types,group_refs,sizes = user.get_groups_belong_to()   
                                    while True:
                                        self.show_group(name, last_name, ids_group, group_names, group_types, group_refs,str(user.user_key))
                                        line = input(line_char)
                                        lines = line.split(" ",1)
                                        line = lines[0]
                                        idgroup = lines[1] if len(lines) > 1 else None
                                        if line == "1" and idgroup:
                                            if idgroup in ids_group:
                                                self.console_cleaned()
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
                                                    print("formato: <Y-M-D HH:MM> - 24 Horas")
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
                                                user.create_groupal_event(ename,date_ini,date_end,idgroup)
                                                break
                                        elif line == "2" and idgroup:
                                            if idgroup in ids_group:
                                                index = ids_group.index(idgroup)
                                                gtype = group_types[index]
                                                gname = group_names[index]
                                                size = sizes[index]
                                                ref = group_refs[index]
                                                if int(ref) == user.user_key:
                                                    self.console_cleaned()
                                                    print("<back>: regresar al perfil")
                                                    print("<home>: volver a la vista principal")
                                                    print("<exit>: cerrar la aplicación")
                                                    print("")
                                                    while line == "2":
                                                        print("Nombre de usuario que desea añadir:")
                                                        username = input(line_char)
                                                        if username == "": continue
                                                        elif username == "exit": line = "exit"
                                                        elif username == "home": line = "home"
                                                        elif username == "back": line = "back"
                                                        username = hash_key(username)
                                                        break
                                                    if line != "2": break
                                                    role = None
                                                    level = None
                                                    while line == "2" and gtype == GType.Hierarchical.value:
                                                        print("Nombre del rol que desea asignarle: (Tenga en cuenta que 'Propietario' no se puede asignar)")
                                                        role = input(line_char)
                                                        if role == "": continue
                                                        elif role == "exit": line = "exit"
                                                        elif role == "home": line = "home"
                                                        elif role == "back": line = "back"
                                                        break
                                                    while line == "2" and gtype == GType.Hierarchical.value:
                                                        print("Nivel jerárquico del rol asignado: (Tenga en cuenta que si ya fue asignado previamente, este nivel no será tomado en cuenta. Si es un rol nuevo, asegúrese de establecer un valor para el nivel entre 0 y 1000)")
                                                        level = input(line_char)
                                                        if level == "": continue
                                                        elif level == "exit": line = "exit"
                                                        elif level == "home": line = "home"
                                                        elif level == "back": line = "back"
                                                        try: level = int(level)
                                                        except: continue
                                                        break
                                                    boolean = user.add_member(idgroup,username,gname,gtype,size,role,level)
                                                    if boolean == False:
                                                        print("Usuario no existente")
                                                        time.sleep(2)
                                                    break
                                                else:
                                                    print("No tiene permiso para añadir miembros. Usted no es el propietario")
                                                    time.sleep(2)
                                        elif line == "3" and idgroup:
                                            if idgroup in ids_group:
                                                index = ids_group.index(idgroup)
                                                creator = group_refs[index]
                                                gname = group_names[index]
                                                gtype = group_types[index]
                                                if gtype == GType.Hierarchical.value:
                                                    ids_members,roles = user.get_inferior_members(int(creator),idgroup,str(user.user_key))
                                                    while True:
                                                        self.show_member(name, last_name,creator,gname, ids_members)
                                                        line = input(line_char)
                                                        lines = line.split(" ",1)
                                                        line = lines[0]
                                                        id_member = lines[1] if len(lines) > 1 else None
                                                        if line == "1" and id_member:
                                                            if id_member in ids_members:
                                                                ids_event,event_names,dates_ini,dates_end,states,visibilities,creators,id_groups,_=user.get_all_events(int(id_member))
                                                                while True:
                                                                    self.show_event(name,last_name,ids_event,event_names,dates_ini,dates_end,states,visibilities,creators,id_groups,id_member)
                                                                    line = input(line_char)
                                                                    if line == "exit" or line == "home" or line == "back": break
                                                            else:
                                                                print("Este miembro no pertenece a la jerarquía inferior")
                                                                time.sleep(2)
                                                        if line == "exit" or line == "home" or line == "back": break            
                                                else:
                                                    print("Se debe realizar esta solicitud en un grupo Jerárquico")
                                                    time.sleep(2)
                                        if line == "exit" or line == "home" or line == "back": break
                                if line == "exit" or line == "home": break
                        else:
                            print("Su nombre de usuario o contraseña son incorrectas. Inténtelo de nuevo")
                            time.sleep(2)
                    if line == "exit" or line == "home": break
                if line == "exit": break 
            if line == "exit": break


sys = System().start_console()