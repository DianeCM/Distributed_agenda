import json
import zipfile
import shutil
import sqlite3
from utils import send_request
import socket
from peewee import *
import struct

# Define el modelo de la tabla
class MiTabla(Model):
    campo1 = CharField()
    campo2 = IntegerField()
    fecha = DateField()

    class Meta:
        database = None

class Another_Tab(Model):
    campo1 = CharField()
    campo2 = IntegerField()
    fecha = DateField()

    class Meta:
        database = None

database = SqliteDatabase('original.db')
MiTabla._meta.database = database
database.create_tables([MiTabla])

Another_Tab._meta.database = database
database.create_tables([Another_Tab])


# Crea una nueva base de datos
conn_copia = SqliteDatabase('copia.db')

MiTabla._meta.database = conn_copia
conn_copia.create_tables([MiTabla])

Another_Tab._meta.database = conn_copia
conn_copia.create_tables([Another_Tab])

MiTabla._meta.database = database
my_table = MiTabla.create(campo1 = "po",campo2 = 2 ,fecha = "2023-09-11" )
my_table.save()

Another_Tab._meta.database = database
my_table = Another_Tab.create(campo1 = "la vie",campo2 = 2 ,fecha = "2023-09-11" )
my_table.save()

# Selecciona solo los registros que deseas copiar
registros1 = MiTabla.select().where((MiTabla.campo2 >= 1))
registros2 = Another_Tab.select().where((Another_Tab.campo1 >= 1))
for register in registros1:
    print(register.campo1)
print("another_tab")
for register in registros2:
    print(register.campo1)
    

# Crea una copia de la base de datos original que solo contiene los registros seleccionados
shutil.copyfile('original.db','copia.db')

# Cierra la conexión a la nueva base de datos
conn_copia.close()

MiTabla._meta.database = conn_copia
registros = MiTabla.select()#.where(MiTabla.fecha >= 1)
print("tabla2")
for register in registros:
    print(register.campo1)

Another_Tab._meta.database = conn_copia
registros = Another_Tab.select()#.where(Another_Tab.fecha >= 1)
print("another_tabla2")
for register in registros:
    print(register.campo1)

# Crea un diccionario con la información que deseas almacenar en el archivo JSON
data = {"nombre": "Juan", "edad": 25, "ciudad": "Buenos Aires"}

# Convierte el diccionario en una cadena JSON
json_data = json.dumps(data)

# Escribe la cadena JSON en un archivo llamado "datos.json"
with open("datos.json", "w") as f:
    f.write(json_data)

# Abre la base de datos SQLite
#conn = sqlite3.connect("original.db")

# Crea una copia de la base de datos
#shutil.copy2("original.db", "copia.db")



# Cierra la conexión a la base de datos
#conn.close()

# Crea un archivo ZIP llamado "datos.zip"
with zipfile.ZipFile("datos.zip", "w") as mi_zip:
    # Agrega el archivo "datos.json" al archivo ZIP
    mi_zip.write("datos.json")
    mi_zip.write("copia.db")

# Abre un socket y conecta con el servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1234))

# Lee los datos del archivo ZIP y envía los datos a través del socket
with open("datos.zip", "rb") as f:
    #while True:
        # Lee los datos del archivo en bloques
        data = f.read()
        
        #if not data:
            # Si no hay más datos, sal del bucle
            #break
        # Envía los datos a través del socket
#data_len = len(data)
#longitud_data = struct.pack('I',data_len)
#s.sendall(data_len)

s.sendall(data)


# Cierra el socket
s.close()