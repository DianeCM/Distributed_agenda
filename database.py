import sqlite3 as sql3

def create_tables():
    # Crear una conexion a la base de datos
    conn = sql3.connect('agenda.db')
    # Crear una tabla
    conn.execute('''CREATE TABLE IF NOT EXISTS person (username VARCHAR(15) PRIMARY KEY, name VARCHAR(15), last_name VARCHAR(40), job VARCHAR(40))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS grouped (id_group INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(15), type VARCHAR(25))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS person_grouped (username VARCHAR(15), id_group INTEGER, PRIMARY KEY (username, id_group))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS event (id_event INTEGER PRIMARY KEY AUTOINCREMENT, date_ini VARCHAR(25), date_end VARCHAR(25))''')
    conn.execute('''CREATE TABLE IF NOT EXISTS person_event (username VARCHAR(15), id_event INTEGER, PRIMARY KEY (username, id_event))''')
    # Guardar los cambios
    conn.commit()
    # Cerrar la conexion a la base de datos
    conn.close()


def insert_element(table:str):
    # Conectar con la base de datos
    conn = sql3.connect('agenda.db')
    # Insertar datos en la tabla
    conn.execute('''INSERT INTO person (username, name, last_name, job) VALUES ('jordipi', 'Jordan', 'Pla Gonzalez', 'MATCOM')''')
    conn.execute('''INSERT INTO grouped (name, type) VALUES ('Mala Compannia', 'jerarquico')''')
    conn.execute('''INSERT INTO grouped (name, type) VALUES ('Buena Compannia', 'no jerarquico')''')
    conn.execute('''INSERT INTO person_grouped (username, id_group) VALUES ('jordipi', 1)''')
    conn.execute('''INSERT INTO event (date_ini, date_end) VALUES ('27/06/23-08:45', '27/06/23-08:16:45')''')
    conn.execute('''INSERT INTO person_event (username, id_event) VALUES ('jordipi', 1)''')
    # Guardar los cambios
    conn.commit()
    # Cerrar la conexion a la base de datos
    conn.close()

def delete_element(table:str):
    # Conectar con la base de datos
    conn = sql3.connect('agenda.db')
    # Codigo aqui
    # Guardar los cambios
    conn.commit()
    # Cerrar la conexion a la base de datos
    conn.close()

def user_events_queries():
    conn = sql3.connect('agenda.db')
    cursor = conn.cursor()
    # Consultar los datos de la tabla
    cursor.execute("SELECT * FROM person_grouped JOIN grouped")
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