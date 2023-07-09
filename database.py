import sqlite3 as sql3

# CREAR LA BASE DE DATOS
def create_tables():
    conn = sql3.connect('agenda.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS person (username VARCHAR(15) PRIMARY KEY, 
                                                    name VARCHAR(15), 
                                                    last_name VARCHAR(40))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS team (id_group INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    name VARCHAR(40),
                                                    propietary VARCHAR(15), 
                                                    type VARCHAR(15))''')
    conn.execute('''CREATE TRIGGER IF NOT EXISTS delete_team AFTER DELETE ON person FOR EACH ROW BEGIN DELETE FROM team WHERE propietary=OLD.username; END;''')
    conn.execute('''CREATE TABLE IF NOT EXISTS group_roles (id_group INTEGER,
                                                    role VARCHAR(40),
                                                    priority INTEGER,
                                                    PRIMARY KEY(id_group, role))''')
    conn.execute('''CREATE TRIGGER IF NOT EXISTS delete_grole AFTER DELETE ON team FOR EACH ROW BEGIN DELETE FROM group_roles WHERE id_group=OLD.id_group; END;''')
    conn.execute('''CREATE TABLE IF NOT EXISTS persons_groups (username VARCHAR(15), 
                                                    id_group INTEGER, 
                                                    role VARCHAR(40), 
                                                    PRIMARY KEY(username, id_group))''')
    conn.execute('''CREATE TRIGGER IF NOT EXISTS delete_pgroup1 AFTER DELETE ON person FOR EACH ROW BEGIN DELETE FROM persons_groups WHERE username=OLD.username; END;''')
    conn.execute('''CREATE TRIGGER IF NOT EXISTS delete_pgroup2 AFTER DELETE ON group_roles FOR EACH ROW BEGIN DELETE FROM persons_groups WHERE id_group=OLD.id_group; END;''')
    conn.execute('''CREATE TRIGGER  IF NOT EXISTS delete_pgroup3 AFTER DELETE ON group_roles FOR EACH ROW BEGIN UPDATE persons_groups SET role="Miembro" WHERE role=OLD.role; END;''')
    conn.execute('''CREATE TABLE IF NOT EXISTS personal_events (id_event INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    username VARCHAR(15),
                                                    name VARCHAR(40), 
                                                    date_ini VARCHAR(25), 
                                                    date_end VARCHAR(25),
                                                    visibility VARCHAR(8),          
                                                    UNIQUE (username, id_event))''')
    conn.execute('''CREATE TRIGGER IF NOT EXISTS delete_pevent AFTER DELETE ON person FOR EACH ROW BEGIN DELETE FROM personal_events WHERE username=OLD.username; END;''')
    conn.execute('''CREATE TABLE IF NOT EXISTS groupal_events (id_event INTEGER PRIMARY KEY AUTOINCREMENT,
                                                    id_group INTEGER,
                                                    name VARCHAR(40),  
                                                    date_ini VARCHAR(25), 
                                                    date_end VARCHAR(25),
                                                    author VARCHAR(15),
                                                    UNIQUE (id_group, id_event))''')
    conn.execute('''CREATE TRIGGER IF NOT EXISTS delete_gevent1 AFTER DELETE ON team FOR EACH ROW BEGIN DELETE FROM groupal_events WHERE id_group=OLD.id_group; END;''')
    conn.execute('''CREATE TRIGGER IF NOT EXISTS delete_gevent2 AFTER DELETE ON person FOR EACH ROW BEGIN DELETE FROM groupal_events WHERE author=OLD.username; END;''')
    conn.execute('''CREATE TABLE IF NOT EXISTS member_events (username VARCHAR(15),
                                                    id_group INTEGER,
                                                    id_event INTEGER,
                                                    PRIMARY KEY (username, id_group, id_event))''')
    conn.execute('''CREATE TRIGGER IF NOT EXISTS delete_mevent1 AFTER DELETE ON person FOR EACH ROW BEGIN DELETE FROM member_events WHERE username=OLD.username; END;''')
    conn.execute('''CREATE TRIGGER IF NOT EXISTS delete_mevent2 AFTER DELETE ON groupal_events FOR EACH ROW BEGIN DELETE FROM member_events WHERE (id_group=OLD.id_group OR id_event=OLD.id_event); END;''')
    conn.commit()
    conn.close()

# CREACION DE CUENTA EN EL SISTEMA INTRODUCE USUARIO A LA BASE DE DATOS
def insert_person(username:str, name:str, last_name:str):
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO person (username, name, last_name) VALUES ('{username}', '{name}', '{last_name}')''')
    conn.commit()
    cursor.close()
    conn.close()

# ELIMINACION DE CUENTA EN EL SISTEMA BORRA USUARIO DE LA BASE DE DATOS CON TODO LO RELACIONADO A SU CUENTA
def delete_person(username:str):
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute(f'''DELETE FROM person WHERE username="{username}"''')
    conn.commit()
    cursor.close()
    conn.close()

# CREACION DE GRUPO POR UN USUARIO EN EL SISTEMA INTRODUCE GRUPO A LA BASE DE DATOS Y LA RELACION USUARIO-GRUPO COMO PROPIETARIO
def insert_group(username:str, name:str, group_type:str):
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO team (name, propietary, type) VALUES ('{name}','{username}','{group_type}')''')
    id_group = cursor.lastrowid
    cursor.execute(f'''INSERT INTO group_roles (id_group, role, priority) VALUES ({id_group},'Propietario',0)''')
    cursor.execute(f'''INSERT INTO group_roles (id_group, role, priority) VALUES ({id_group},'Miembro',10000000)''')
    cursor.execute(f'''INSERT INTO persons_groups (username, id_group, role) VALUES ('{username}','{id_group}','Propietario')''')
    conn.commit()
    cursor.close()
    conn.close()

# ELIMINACION DE GRUPO EN EL SISTEMA BORRA GRUPO DE LA BASE DE DATOS Y TODO LO RELACIONADO USUARIO-GRUPO y EVENTO-GRUPO
def delete_group(id_group:int):
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute(f'''DELETE FROM team WHERE id_group={id_group}''')
    conn.commit()
    cursor.close()
    conn.close()

# CREACION DE ROL POR PROPIETARIO DE GRUPO JERARQUICO EN EL SISTEMA
#*************************************************************modif name (mod gro_per kien tenia ese role) and prior
def insert_role(id_group:int, name:str, priority:int):
    if 0 < priority < 10000000:
        conn = sql3.connect('agenda.db')
        cursor = conn.cursor()
        cursor.execute(f'''INSERT INTO group_roles (id_group, role, priority) VALUES ({id_group},'{name}',{priority})''')
        conn.commit()
        cursor.close()
        conn.close()
    else:
        raise print("La prioridad debe ser mayor que 0")

# ELIMINACION DE ROL POR PROPIETARIO DE GRUPO JERARQUICO EN EL SISTEMA
def delete_role(id_group:int, name:str):
    if name != "Miembro" or name != "Propietario":
        conn = sql3.connect('agenda.db')
        cursor = conn.cursor()
        cursor.execute(f'''DELETE FROM group_roles WHERE (id_group={id_group} AND role='{name}')''')
        conn.commit()
        cursor.close()
        conn.close()
    else:
        raise print("No se puede eliminar roles bases")

# AÑADIR MIEMBROS A GRUPO POR PROPIETARIO EN EL SISTEMA INTRODUCE LA RELACION USUARIO-GRUPO COMO MIEMBRO
def insert_person_to_group(username:str, id_group:int):
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO persons_groups (username, id_group, role) VALUES ('{username}',{id_group},'Miembro')''')
    conn.commit()
    cursor.close()
    conn.close()

# ELIMINACION DE MIEMBRO DE GRUPO EN EL SISTEMA BORRA LA RELACION USUARIO-GRUPO Y PIERDE ACCESO A LOS EVENTOS
def delete_person_from_group(username:str, id_group:int):
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute(f'''DELETE FROM persons_groups WHERE (id_group={id_group} AND username="{username}")''')
    conn.commit()
    cursor.close()
    conn.close()

#**********************************************************mod role a miembro especifico en g jerarquico

# AÑADIR EVENTO PERSONAL POR EL USUARIO EN EL SISTEMA
#********************************************************mod name, dates y vis
def insert_personal_event(username:str, name:str, date_ini:str, date_end:str, visibility:str='Público'):
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO personal_events (username, name, date_ini, date_end, visibility) VALUES ('{username}','{name}','{date_ini}','{date_end}','{visibility}')''')
    conn.commit()
    cursor.close()
    conn.close()

# ELIMINACION DE EVENTO PERSONAL POR EL USUARIO EN EL SISTEMA
def delete_personal_event(username:str, id_event:int):
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute(f'''DELETE FROM personal_events WHERE (id_event={id_event} AND username="{username}")''')
    conn.commit()
    cursor.close()
    conn.close()

# AÑADIR EVENTO GRUPAL POR USUARIO/MIEMBRO DE GRUPO (JERARQUICO/NO JERARQUICO) EN EL SISTEMA
#********************************************************mod name, dates
def insert_groupal_event(id_group:str, name:str, date_ini:str, date_end:str, author:str):
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO groupal_events (id_group, name, date_ini, date_end, author) VALUES ({id_group},'{name}','{date_ini}','{date_end}','{author}')''')
    id_event = cursor.lastrowid
    cursor.execute(f'''SELECT type FROM team WHERE id_group={id_group}''')
    row = cursor.fetchall()
    if row[0] == "Jerárquico":
        # SELECT id_role, username FROM persons_groups JOIN role_groups ON pg.id_group = rg.id_group WHERE pg.id_group={id_group}
        # BUSCAR TODOS LOS USERNAME TAL QUE YO COMO AUTHOR SEA SUPERIOR EN EL ROLE JOIN INDEX ROLE
        # NO ME AGREGO AL EVENTO
        print()
    else:
        # SELECT username FROM persons_groups WHERE id_group={id_group}
        # username = [row[0] for row in rows]
        print()
    #cursor.execute(f'''INSERT INTO member_events (username, id_group, id_event) VALUES ('{username}',{id_group},{id_event})''')
    conn.commit()
    cursor.close()
    conn.close()

# ELIMINACION DE EVENTO GRUPAL POR EL AUTOR DEL EVENTO EN EL SISTEMA
def delete_groupal_event(username:str, id_event:int):
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute(f'''DELETE FROM groupal_events WHERE (id_event={id_event} AND author="{username}")''')
    conn.commit()
    cursor.close()
    conn.close()


# MODIFICACIONES, CONSULTAS

def user_events_queries():
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    # Consultar los datos de la tabla
    cursor.execute("SELECT * FROM person_grouped JOIN grouped ON person_grouped.id_group = grouped.id_group")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # Cerrar la conexion a la base de datos
    conn.close()

def user_per_group_low_rank_queries():
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person_grouped JOIN grouped")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # Cerrar la conexion a la base de datos
    conn.close()

def colision_queries():
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person_grouped JOIN grouped")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # Cerrar la conexion a la base de datos
    conn.close()

def group_per_user_queries():
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM person_grouped JOIN grouped")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # Cerrar la conexion a la base de datos
    conn.close()


create_tables()
insert_person("jordipi", "Jordan", "Pla Gonzalez")
insert_person("dianecm", "Dianelys", "Cruz Mengana")
insert_group("jordipi", "Mala", "Jerárquico")
insert_group("dianecm", "Buena", "Jerárquico")
insert_personal_event("dianecm", "Boda de Tia","3/7/23-08:45","3/7/23-16:00")
insert_personal_event("dianecm", "Quince de Prima","4/7/23-08:45","4/7/23-16:00")
insert_personal_event("jordipi", "Boda de Hermana","3/7/23-08:45","3/7/23-16:00")
insert_person_to_group("dianecm", 1)
conn = sql3.connect('agenda.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM person")
rows = cursor.fetchall()
print("Person")
for row in rows:
    print(row)
cursor.execute("SELECT * FROM team")
rows = cursor.fetchall()
print("Group")
for row in rows:
    print(row)
cursor.execute("SELECT * FROM group_roles")
rows = cursor.fetchall()
print("Roles")
for row in rows:
    print(row)
cursor.execute("SELECT * FROM persons_groups")
rows = cursor.fetchall()
print("Person x Groups")
for row in rows:
    print(row)
cursor.execute("SELECT * FROM personal_events")
rows = cursor.fetchall()
print("Person x Events")
for row in rows:
    print(row)
delete_person("jordipi")
cursor.execute(f'''DELETE FROM group_roles WHERE role="Capitan"''')
conn.commit()
print()

cursor.execute("SELECT * FROM person")
rows = cursor.fetchall()
print("Person")
for row in rows:
    print(row)
cursor.execute("SELECT * FROM team")
rows = cursor.fetchall()
print("Group")
for row in rows:
    print(row)
cursor.execute("SELECT * FROM group_roles")
rows = cursor.fetchall()
print("Roles")
for row in rows:
    print(row)
cursor.execute("SELECT * FROM persons_groups")
rows = cursor.fetchall()
print("Person x Groups")
for row in rows:
    print(row)
cursor.execute("SELECT * FROM personal_events")
rows = cursor.fetchall()
print("Person x Events")
for row in rows:
    print(row)
conn.close()