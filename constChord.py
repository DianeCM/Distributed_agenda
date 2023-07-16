LOOKUP_REQ = '1'
LOOKUP_REP = '2'
JOIN_REQ   = '3'
JOIN_REP   = '4'
LEAVE      = '5'
DISCOVER   = '6'
STOP       = '7'
MOV_DATA_REQ  = '8'
MOV_DATA_REP  = '9'
ACEPT_PRED = '10'
ACEPT_SUC  = '11'
GET_NODES  = '12'
CHECK_REQ  = '13'
CHECK_REP  = '14' 
SET_LEADER = '15'
REP_DATA_REQ = '16'
REP_DATA_REP = '17'
SET_DATA_REQ = '18'
SET_DATA_REP = '19'
SET_REP_DATA_REQ = '20'
GET_DATA_REQ  = '21'
GET_DATA_REP  = '22'
SET_NODES = '23'

#Creates and Updates
CREATE_PROFILE = '30'
REP_PROFILE = '31'
CREATE_GROUP = '32'
REP_GROUP = '33'
CREATE_PEVENT = '34'  # ESTE LO AGREGUE
REP_PEVENT = '35'
CREATE_GEVENT = '36'  # ESTE LO AGREGUE


ACEPT_EVENT = '40'  # ESTE LO AGREGUE
DECLINE_EVENT = '41'  # ESTE LO AGREGUE
ADD_MEMBER = '42'  # ESTE LO AGREGUE

#delete
# DELETE_PROFILE = '50'
# DELETE_GROUP = '51'
DELETE_EVENT = '52'
DELETE_NOTIFICATION = '54'  # ESTE LO AGREGUE


#Queries
GET_PROFILE = '60'
GET_PROFILE_RESP = '61'
GET_NOTIFICATIONS = '62' # ESTE LO AGREGUE
GET_NOTIF_RESP = '63'
GET_EVENTS = '64' # ESTE LO AGREGUE
GET_EVENTS_RESP = '65'
GET_HIERARCHICAL_MEMBERS = '66' # ESTE LO AGREGUE
GET_HIER_MEMB_RESP = '67'
GET_EVENTS_MEMBER = '68' # ESTE LO AGREGUE
GET_EVENT_MEMB_RESP = '69'
GET_GROUPS = '70' # ESTE LO AGREGUE
GET_GROUPS_RESP = '71'
SHOW_MSGS = '72'
SHOW_MSGS_RESP = '73'

from peewee import *
import datetime

db = SqliteDatabase('my_database.db')

class MyModel(Model):
    date_field = DateTimeField()

    class Meta:
        database = db

# Creamos una instancia de nuestro modelo
my_model = MyModel()

# Obtenemos la fecha actual
now = datetime.datetime.now()

# Asignamos la fecha actual al campo de fecha en nuestro modelo
my_model.date_field = now

# Convertimos la fecha a una cadena de texto usando el método strftime()
date_string = now.strftime('%Y-%m-%d %H:%M:%S')

# Imprimimos la cadena de texto
print(date_string)