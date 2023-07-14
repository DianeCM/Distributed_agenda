from utils import *

key1 = hash_key("yumilka")

key2 = hash_key("yumilka")

key1 = key1.to_bytes(20, byteorder='big')

print(key1 == key2)

key3 = int.from_bytes(key1, byteorder='big')

print(key3 == key2)

value = str(key3)
print(int(value) == key2)
print(value)

# import json
# import zipfile
# import socket
# import io
# from peewee import *
# import shutil

# # Define el modelo de la tabla
# class MiTabla(Model):
#     campo1 = BlobField()
#     campo2 = IntegerField()
#     fecha = DateField()

#     class Meta:
#         database = None

# class Another_Tab(Model):
#     campo1 = CharField()
#     campo2 = IntegerField()
#     fecha = DateField()

#     class Meta:
#         database = None


# database = SqliteDatabase('original.db')
# MiTabla._meta.database = database
# database.create_tables([MiTabla])
# my_table = MiTabla.create(campo1 = key1,campo2 = 21 ,fecha = "2024-09-11" )
# my_table.save()

# register = MiTabla.select().where(MiTabla.campo1 == key2.to_bytes(20, byteorder='big'))
# for reg in register:
#     print(reg)