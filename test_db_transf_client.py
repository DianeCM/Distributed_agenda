import json
import zipfile
import socket
import io
from peewee import *
import shutil

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
my_table = MiTabla.create(campo1 = "popoporeso",campo2 = 21 ,fecha = "2024-09-11" )
my_table.save()

Another_Tab._meta.database = database
database.create_tables([Another_Tab])
another_tab = Another_Tab.create(campo1 = "popoporeso",campo2 = 21 ,fecha = "2024-09-11" )
another_tab.save()

# Crea un socket y espera por una conexión entrante
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 1234))
s.listen()

# Acepta la conexión entrante
conn, addr = s.accept()
data = conn.recv(1000000)
data = b''+ data
print(type(data))

conn.close()
s.close()

with zipfile.ZipFile(io.BytesIO(data),'r') as my_zip:
    my_zip.extractall()
    file = my_zip.read("copia.db")
    data = SqliteDatabase(file)
    print(data)

# copy the contents of each table from the attached database to the main database
#for table in data.get_tables():
#    database.execute_sql(f'INSERT INTO original.{table} SELECT * FROM attached.{table}')

# detach the attached database from the main database
#database.execute_sql('DETACH DATABASE attached')

shutil.copyfile('copia.db','original.db')
# Cierra la conexión y el socket


registers = MiTabla.select()
for reg in registers:
    print(reg.campo1)

print("another_tab")
registers = Another_Tab.select()
for reg in registers:
    print(reg.campo1)

# Descomprime el archivo ZIP
#with zipfile.ZipFile("archivo_recibido.zip", "r") as mi_zip:
#    mi_zip.extractall()

# Abre el archivo ZIP llamado "datos.zip"
#with zipfile.ZipFile(data, "r") as mi_zip:
    # Extrae el archivo "datos.json" del archivo ZIP en el directorio actual
    #mi_zip.extract("datos.json")
    #mi_zip.extract("copia.db")
#    mi_zip.extractall()