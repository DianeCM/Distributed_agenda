from peewee import *
from enum import Enum
from utils import *


class Account(Model):
    user = CharField(max_length=70,null=False, unique=True, primary_key=True)
    name = CharField(max_length=15, null=False)
    last = CharField(max_length=50, null=False)
    passw = CharField(max_length=40, null=False)

def filter_function(condition,cls):
            def cond(row):
                key = row.user 
                return condition(key)
            return cond

condition = lambda key: key >0

conn_copia = SqliteDatabase("cool.db")

Account._meta.database = conn_copia
conn_copia.create_tables([Account])
my_table = Account.create(user = "la vie",name = "p" ,last = "2023-09-11", passw="lol" )
my_table.save()

reg = Account.select().where((filter_function(condition,Account)))

for r in reg:
       print(r)