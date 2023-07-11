from peewee import *
from enum import Enum
from utils import hash_key

class Privacity(Enum):
    Public = "Público"
    Private = "Privado"

class GType(Enum):
    Hierarchical = "Jerárquico"
    Non_hierarchical = "No Jerárquico"

class State(Enum):
    Asigned = "Asignado"
    Pendient = "Pendiente"
    Personal = "Personal"

class Account(Model):
    iduser = BlobField(null=False, unique=True, primary_key=True)
    name = CharField(max_length=15, null=False)
    last = CharField(max_length=40, null=False)
    password = CharField(max_length=50, null=False)

    class Meta:
        database = None


class Notification(Model):
    user = ForeignKeyField(Account, on_delete='CASCADE')
    idnotif = BigIntegerField(null=False)
    text = CharField(max_length=300)

    class Meta:
        database = None
        primary_key = CompositeKey('user', 'idnotif')
        autoincremental = 1

    def save(self, *args, **kwargs):
        if not self.idnotif:
            self.idnotif = Notification._meta.autoincremental
            Notification._meta.autoincremental += 1
        Model.save(self, *args, **kwargs)


class Group(Model):
    creator = ForeignKeyField(Account, on_delete='CASCADE')
    idgroup = BlobField(null=False, unique=True, primary_key=True)
    gname = CharField(max_length=50, null=False)
    gtype = CharField(max_length=15, null=False)
    description = CharField(max_length=100, null=True)

    class Meta:
        database = None
        autoincremental = 1

    def save(self, *args, **kwargs):
        if self.idgroup is None:
            id_current = Group._meta.autoincremental
            creator = int.from_bytes(self.creator.iduser,byteorder='big')
            id_current = hash_key(f'{creator}_{id_current}')
            self.idgroup = id_current.to_bytes(20, byteorder='big')
            Group._meta.autoincremental += 1
        Model.save(self, *args, **kwargs)


class MemberGroup(Model):
    user = ForeignKeyField(Account, on_delete='CASCADE')
    idgroup = BlobField(null=False)
    idref = BlobField(null=False)

    class Meta:
        database = None
        primary_key = CompositeKey('user','idgroup')


class MemberAccount(Model):
    group = ForeignKeyField(Group, on_delete='CASCADE')
    iduser = BlobField(null=False)
    role = CharField(max_length=50, null=False)
    level = IntegerField(null=False)

    class Meta:
        database = None
        primary_key = CompositeKey('group','iduser')


class Event(Model):
    user = ForeignKeyField(Account, on_delete='CASCADE')
    idevent = BlobField(null=False)
    ename = CharField(max_length=100, null=False)
    date_ini = DateTimeField(null=False)
    date_end = DateTimeField(null=False)
    state = CharField(max_length=9, null=False)
    visibility = CharField(max_length=9, null=False)
    idcreator = BlobField(null=False)
    idgroup = BlobField(null=True)
    
    class Meta:
        database = None
        primary_key = CompositeKey('user', 'idevent')
        autoincremental = 1

    def save(self, *args, **kwargs):
        if not self.idevent:
            id_current = Event._meta.autoincremental
            user = int.from_bytes(self.user.iduser,byteorder='big')
            id_current = hash_key(f'{user}_{id_current}')
            self.idevent = id_current.to_bytes(20, byteorder='big')
            Event._meta.autoincremental += 1
        Model.save(self, *args, **kwargs)


class NodeYumi:
    def __init__(self, id: int):
        db_name = f"{id}.db"
        self.database = SqliteDatabase(db_name)
        for cls in [Account, Notification, Group, MemberGroup, MemberAccount, Event]:
            cls._meta.database = self.database
            if not cls.table_exists():
                self.database.create_tables([cls])

    def create_account(self, userkey: int, name: str, last_name: str, password: str):
        userkey = userkey.to_bytes(20, byteorder='big')
        account = Account.create(iduser=userkey, name=name, last=last_name, password=password)
        account.save()

    def delete_account(self, userkey: int):
        userkey = userkey.to_bytes(20, byteorder='big')
        account = Account.get(iduser=userkey)
        account.delete_instance(recursive=True)

    def add_notification(self, userkey: int, notification: str):
        userkey = userkey.to_bytes(20, byteorder='big')
        account = Account.get(iduser=userkey)
        notif = Notification.create(user=account, text=notification)
        notif.save()

    def show_notification(self, userkey: int):
        userkey = userkey.to_bytes(20, byteorder='big')
        registers = Notification.select().where(Notification.user == userkey).order_by(Notification.idnotif.desc())
        for register in registers:
            print(register.idnotif, register.text)

    def delete_notification(self, userkey: int, idnotif: int):
        userkey = userkey.to_bytes(20, byteorder='big')
        notif = Notification.get((Notification.user == userkey) & (Notification.idnotif == idnotif))
        notif.delete_instance(recursive=True)

    def create_group(self, userkey:int, name: str, gtype: GType, description: str = ""):
        userkeyn = userkey.to_bytes(20, byteorder='big')
        account = Account.get(iduser=userkeyn)
        group = Group.create(creator=account, gname=name, gtype=gtype.value, description=description)
        group.save()
        self.add_member_group(userkey, group.idgroup, userkeyn)
        self.add_member_account(group.idgroup, userkey, "Propietario")

    def show_user_group_created(self, userkey: int):
        userkey = userkey.to_bytes(20, byteorder='big')
        registers = Group.select().where(Group.creator == userkey)
        for register in registers:
            print(register.idgroup, register.gname, register.gtype)

    def show_user_in_group(self, userkey: int):
        userkey = userkey.to_bytes(20, byteorder='big')
        registers = MemberAccount.select().where(MemberAccount.iduser == userkey)
        for register in registers:
            print(register.group, register.role)

    def delete_group(self, userkey: int, id_group: bytes):
        userkey = userkey.to_bytes(20, byteorder='big')
        group = Group.get((Group.idgroup == id_group) & (Group.creator == userkey))
        if group: group.delete_instance(recursive=True)
        
    def add_member_group(self, userkey:int, idgroup:bytes, idref:bytes):
        userkey = userkey.to_bytes(20, byteorder='big')
        account = Account.get(iduser=userkey)
        member = MemberGroup.create(user=account, idgroup=idgroup, idref=idref)
        member.save()
    
    def add_member_account(self, idgroup:bytes, userkey: int, role='Miembro', level:int=0):
        group = Group.get(idgroup=idgroup)
        userkey = userkey.to_bytes(20, byteorder='big')
        if role == 'Propietario':
            role_level = None
            try:
                role_level = MemberAccount.get((MemberAccount.group==group)&(MemberAccount.role==role))
            except:
                asign = MemberAccount.create(group=group, iduser=userkey, role=role, level=0)
                asign.save()
            if role_level is not None:
                print("Solo puede haber un propietario")
        elif role == 'Miembro':
            asign = MemberAccount.create(group=group, iduser=userkey, role=role, level=1000)
            asign.save()
        else:
            if group.gtype == GType.Hierarchical.value:
                role_level = None
                try:
                    role_level = MemberAccount.get((MemberAccount.group==group)&(MemberAccount.role==role))
                except:
                    if level is not None and (0 < level < 1000):
                        asign = MemberAccount.create(group=group, iduser=userkey, role=role, level=level)
                        asign.save()
                    else:
                        print("Debe asignar un valor de nivel al rol")
                if role_level:
                    asign = MemberAccount.create(group=group, iduser=userkey, role=role, level=role_level.level)
                    asign.save()
            else: print("Este grupo no acepta roles")

    def create_event_personal(self, userkey: int, name:str, date_ini:str, date_end:str, privacity:Privacity=Privacity.Public, idgroup:bytes=None):
        userkey = userkey.to_bytes(20, byteorder='big')
        account = Account.get(iduser=userkey)
        event = Event.create(user=account, ename=name, date_ini=date_ini, date_end=date_end, state=State.Personal, 
                            visibility=privacity, idcreator=userkey, idgroup=idgroup)
        event.save()

    def create_event_grupal(self, userkey: int, name:str, date_ini:str, date_end:str, privacity:Privacity=Privacity.Public, idgroup:bytes=None):
        userkey = userkey.to_bytes(20, byteorder='big')
        account = Account.get(iduser=userkey)
        event = Event.create(user=account, ename=name, date_ini=date_ini, date_end=date_end, state=State.Pendient, 
                            visibility=privacity, idcreator=account.userid, idgroup=idgroup)
        event.save()

    def show_pendient_events(self):
        Event._meta.database = self.database
        true_id = self.id.to_bytes(20, byteorder='big')
        registers = Event.select().where((Event.user == true_id)&(Event.state==State.Pendient))
        for register in registers:
            print(register.ename, register.date_ini, register.date_end)

    def show_all_events(self):
        Event._meta.database = self.database
        true_id = self.id.to_bytes(20, byteorder='big')
        registers = Event.select().where(Event.user == true_id)
        for register in registers:
            print(register.ename, register.date_ini, register.date_end, register.state)

    def acept_event(self, idevent:bytes):
        Event._meta.database = self.database
        event = Event.get(idevent=idevent)
        event.state = State.Asigned
        event.save()

    def decline_event(self, idevent:bytes):
        # LLAMAR A TO EL MUNDOS
        pass

    def delete_event(self, idevent:bytes):
        Event._meta.database = self.database
        registers = Event.get((Event.idevent == idevent)&(Event.state == State.Personal))
        if registers: registers.delete_instance(recursive=True)
        

    def colision_queries():  # APROBADO
        conn = sql3.connect('agenda.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM person_grouped JOIN grouped")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        # Cerrar la conexion a la base de datos
        conn.close()

    def group_per_user_queries():  # APROBADO
        conn = sql3.connect('agenda.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM person_grouped JOIN grouped")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        # Cerrar la conexion a la base de datos
        conn.close()

    def group_rank():  # APROBADO
        conn = sql3.connect('agenda.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM person_grouped JOIN grouped")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        # Cerrar la conexion a la base de datos
        conn.close()

# TEST CASE
user1 = hash_key("jordipi")
user2 = hash_key("dianecm")
node1 = NodeYumi(hash_key("12345654535653555525625363565464473763563"))
node1.create_account(user1,"Jordan", "Pla Gonzalez","esmionotuyo")
node1.create_account(user2,"Dianelys", "Cruz Mengana","mecagoento")

node1.add_notification(user1,"Tienes un evento que colisiona")
node1.add_notification(user1,"Tienes pendiente de aceptacion un evento")
node1.add_notification(user2,"Tienes un evento que colisiona")
node1.add_notification(user2,"Tienes pendiente de aceptacion un evento")

print('SHOW NOTIF JORDIPI')
node1.show_notification(user1)
print()
print('SHOW NOTIF DIANECM')
node1.show_notification(user2)
print()
print('SHOW NOTIF JORDIPI 1 AFTER DELETE NOTIF 1')
node1.delete_notification(user1,1)
node1.show_notification(user1)

node1.create_group(user1,'Mala Compannia', GType.Hierarchical, 'Esto no es nah')
node1.create_group(user2,'Buena Compannia', GType.Non_hierarchical)
node1.create_group(user1,'Media Compannia', GType.Non_hierarchical, 'Esto no es nah')
print()
print('SHOW GROUP JORDIPI CREATED')
node1.show_user_group_created(user1)

node1.delete_group(user1,b'?\xe6\xc19\xa9m\xc7\xcd\xd8}\xa8\x95\xaf49\x92\xbf\x01\x1dF')
node1.create_group(user1,'Mala Compannia', GType.Hierarchical, 'Esto no es nah')
print()
print('SHOW GROUP JORDIPI CREATED AFTER DELETE GROUP 1')
node1.show_user_group_created(user1)

print()
print('SHOW GROUP DIANECM CREATED')
node1.show_user_group_created(user2)

node1.add_member_account(b'w\xd9NI\xbfi\xd9\x1f\xc4"\xf0\xa7\x91b\xe4\xd0\xfe\xff\xb0\xda',user2)
node1.add_member_account(b'!.\x95\xe4\x9eO\xfbv\x12\x8f\xa4\xc4\r\xc5\x98\x02\x11\xf2\xafb',user2,"Capitan",15)
node1.add_member_account(b'\xc9\x12\xab\xaf\xd7\x0fmB\xd3\x98l\xd9\x96\x8f\x03\x19X{h\xbc',user1)
print()
print('SHOW ALL GROUP JORDIPI BELONG')
node1.show_user_in_group(user1)

node1.create_event_personal(user1,'Boda de Primo','12/7/23-08:35','12/7/23-14:35')
node1.create_event_personal(user1,'Cumple de Hermana','17/7/23-08:35','17/7/23-14:35')
node1.create_event_personal(user1,'Evento Benefico','18/8/23-08:35','19/8/23-14:35')