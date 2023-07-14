from peewee import *
from enum import Enum
from utils import *
import shutil

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
    user = CharField(max_length=70,null=False, unique=True, primary_key=True)
    name = CharField(max_length=15, null=False)
    last = CharField(max_length=50, null=False)
    passw = CharField(max_length=40, null=False)

    class Meta:
        database = None


class Notification(Model):
    user = CharField(max_length=70,null=False)
    notif = BigIntegerField(null=False)
    text = CharField(max_length=300)

    class Meta:
        database = None
        primary_key = CompositeKey('user', 'notif')
        autoincremental = 1

    def save(self, *args, **kwargs):
        if not self.notif:
            self.notif = Notification._meta.autoincremental
            Notification._meta.autoincremental += 1
        Model.save(self, *args, **kwargs)


class Group(Model):
    creator = CharField(max_length=70,null=False)
    group = CharField(max_length=70,null=False, unique=True, primary_key=True)
    gname = CharField(max_length=50, null=False)
    gtype = CharField(max_length=15, null=False)
    descr = CharField(max_length=100, null=True)

    class Meta:
        database = None
        autoincremental = 1

    def save(self, *args, **kwargs):
        if self.group is None:
            idcurrent = Group._meta.autoincremental
            creator = int(self.creator)
            idcurrent = hash_key(f'{creator}_{idcurrent}')
            self.group = str(idcurrent)
            Group._meta.autoincremental += 1
        Model.save(self, *args, **kwargs)


class MemberAccount(Model):
    user = CharField(max_length=70,null=False)
    group = CharField(max_length=70,null=False)
    gtype = CharField(max_length=15, null=False)
    ref = CharField(max_length=70,null=False)

    class Meta:
        database = None
        primary_key = CompositeKey('user','group')


class MemberGroup(Model):
    group = CharField(max_length=70,null=False)
    user = CharField(max_length=70,null=False)
    role = CharField(max_length=50, null=False)
    level = IntegerField(null=False)

    class Meta:
        database = None
        primary_key = CompositeKey('group','user')


class Event(Model):
    user = CharField(max_length=70,null=False)
    event = CharField(max_length=70,null=False)
    ename = CharField(max_length=100, null=False)
    datec = DateTimeField(null=False)
    datef = DateTimeField(null=False)
    state = CharField(max_length=9, null=False)
    visib = CharField(max_length=9, null=False)
    creator = CharField(max_length=70,null=False)
    group = CharField(max_length=70,null=True)
    
    class Meta:
        database = None
        primary_key = CompositeKey('user', 'event')
        autoincremental = 1

    def save(self, *args, **kwargs):
        if not self.event:
            idcurrent = Event._meta.autoincremental
            user = int(self.user)
            idcurrent = hash_key(f'{user}_{idcurrent}')
            self.event = str(idcurrent)
            Event._meta.autoincremental += 1
        Model.save(self, *args, **kwargs)


class DBModel:
    def __init__(self, id: int):
        self.db_name = f"{id}.db"
        self.database = SqliteDatabase(self.db_name)
        self.classes = [Account, Notification, Group, MemberAccount,MemberGroup, Event]
        for cls in self.classes:
            cls._meta.database = self.database
            if not cls.table_exists():
                self.database.create_tables([cls])

    def create_account(self, userkey: int, name: str, last_name: str, password: str):
        userkeyn = str(userkey)
        account = Account.create(user=userkeyn, name=name, last=last_name, passw=password)
        account.save()

    def get_account(self, userkey: int, password: str):
        userkeyn = str(userkey)
        try: user = Account.get((Account.user == userkeyn) & (Account.passw == password))
        except DoesNotExist: return False # DATA => MESS=FALSE, NAME=NONE, LASTNAME=NONE
        return True, user.name, user.last

    # PENDIENTE A CORREGIR
    def delete_account(self, userkey: int):
        userkey = userkey.to_bytes(20, byteorder='big')
        Account.delete().where(Account.user==userkey).execute()
        Notification.delete().where(Notification.user==userkey).execute()
        Event.delete().where(Event.user==userkey).execute()
        Group.delete().where(Group.creator==userkey).execute()
        MemberAccount.delete().where(MemberAccount.user==userkey).execute()
        MemberGroup.delete().where(MemberGroup.user==userkey).execute()
        id_notif = []
        for ids in Notification.select(Group.notif).where(Group.creator == userkey).tuples():
            id_notif.append(ids[0])
            notif = Notification.get(notif=ids[0])
            notif.delete_instance()
        Event.delete().where(Event.user==userkey).execute()
        # BORRAR LOS GRUPOS QUE CREO Y POR CADA UNO DE ESTOS GRUPOs (A CADA UNO DE SUS MIEMBROS ELIMINAR PERTENENCIA GRUPO)
        # ELIMINAR DE LOS GRUPOS QUE LO TIENEN COMO MIEMBRO

    def add_notification(self, userkey: int, text: str, notif: int = None):
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist: return
        notif = Notification.create(user=userkeyn, notif=notif, text=text)
        notif.save()

    def show_notification(self, userkey: int):
        userkeyn = str(userkey)
        registers = Notification.select().where(Notification.user == userkeyn).order_by(Notification.notif.desc())
        for register in registers:
            print(register.notif, register.text)

    def delete_notification(self, userkey: int, notif: int):
        userkeyn = str(userkey)
        try: notif = Notification.get((Notification.user == userkeyn) & (Notification.notif == notif))
        except DoesNotExist: return
        notif.delete_instance(recursive=True)

    def create_group(self, userkey:int, name: str, gtype: GType, description: str = "", group: str = None):
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist: return
        group = Group.create(creator=userkeyn, group=group, gname=name, gtype=gtype.value, description=description)
        group.save()
        self.add_member_account(userkey, group.group, userkeyn)
        self.add_member_group(group.group, userkey, "Propietario")

    def show_group_belong_to(self, userkey: int):
        userkey = userkey.to_bytes(20, byteorder='big')
        registers = MemberAccount.select().where(MemberAccount.user == userkey)
        for register in registers:
            print(register.group)
    
    def show_user_in_group(self, group: bytes):
        registers = MemberGroup.select().where(MemberGroup.group == group)
        for register in registers:
            print(register.user, register.role)

    def delete_group(self, userkey: int, id_group: bytes):
        userkey = userkey.to_bytes(20, byteorder='big')
        group = Group.get((Group.group == id_group) & (Group.creator == userkey))
        if group: group.delete_instance(recursive=True)
        
    def add_member_account(self, userkey:int, idgroup:bytes, idref:bytes):
        userkey = userkey.to_bytes(20, byteorder='big')
        account = Account.get(user=userkey)
        member = MemberAccount.create(user=account, group=idgroup, ref=idref)
        member.save()
    
    def add_member_group(self, idgroup:bytes, userkey: int, role='Miembro', level:int=0):
        group = Group.get(group=idgroup)
        userkey = userkey.to_bytes(20, byteorder='big')
        if role == 'Propietario':
            role_level = None
            try:
                role_level = MemberGroup.get((MemberGroup.group==group)&(MemberGroup.role==role))
            except:
                asign = MemberGroup.create(group=group, user=userkey, role=role, level=0)
                asign.save()
            if role_level is not None:
                print("Solo puede haber un propietario")
        elif role == 'Miembro':
            asign = MemberGroup.create(group=group, iduser=userkey, role=role, level=1000)
            asign.save()
        else:
            if group.gtype == GType.Hierarchical.value:
                role_level = None
                try:
                    role_level = MemberGroup.get((MemberGroup.group==group)&(MemberGroup.role==role))
                except:
                    if level is not None and (0 < level < 1000):
                        asign = MemberGroup.create(group=group, iduser=userkey, role=role, level=level)
                        asign.save()
                    else:
                        print("Debe asignar un valor de nivel al rol")
                if role_level:
                    asign = MemberGroup.create(group=group, iduser=userkey, role=role, level=role_level.level)
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


    def get_filtered_db(self,condition,new_db_name):
        registers = {}
        for cls in self.classes:
            cls._meta.database = self.database
            registers[cls] = cls.select().where((condition(int(cls.user))))
            
        registers.append(Account.select().where((condition(Account.user))))
        registers.append(Notification.select().where((condition(Notification.user))))
        registers.append(Group.select().where((condition(Group.creator))))
        registers.append(MemberGroup.select().where((condition(MemberGroup.user))))
        regsiter_event  =  Event.select().where((condition(Event.user)))

         # Crea una nueva base de datos
        conn_copia = SqliteDatabase(new_db_name)

        for cls in self.classes:
            cls._meta.database = conn_copia
            conn_copia.create_tables([cls])

        shutil.copyfile(self.db_name,new_db_name)
        conn_copia.close()

    def replicate_db(self,db_name):
        copy_db =  SqliteDatabase(db_name)

        for cls in self.classes:
            cls._meta.database = self.database
            rows = list(cls.select())
            with copy_db.atomic():
                cls.bulk_create(rows)
        copy_db.close()

    def check_db(self):
        registers=[]
        for cls in self.classes:
            cls._meta.database = self.database
            registers.append(cls.select())
        for reg in registers[0]:
                print(reg.user,reg.name,reg.last,reg.passw)
        for reg in registers[1]:
                print(reg.user,reg.notif,reg.text)       
        for reg in registers[2]:
                print(reg.creator,reg.group,reg.gname,reg.gtype,reg.descr)       
        for reg in registers[3]:
                print(reg.user,reg.group,reg.ref)   
        for reg in registers[4]:
                print(reg.group,reg.user,reg.role,reg.level) 
        for reg in registers[5]:
                print(reg.user,reg.event,reg.ename,reg.datec,reg.datef,reg.state,reg.visib,reg.creator,reg.group)  

# TEST CASE
user1 = hash_key("jordipi")
user2 = hash_key("dianecm")
node1 = DBModel(hash_key("12345654535653555525625363565464473763563"))
node1.create_account(user1,"Jordan", "Pla Gonzalez","esmionotuyo")
node1.create_account(user2,"Dianelys", "Cruz Mengana","mecagoento")

# node1.add_notification(user1,"Tienes un evento que colisiona")
# node1.add_notification(user1,"Tienes pendiente de aceptacion un evento")
# node1.add_notification(user2,"Tienes un evento que colisiona")
# node1.add_notification(user2,"Tienes pendiente de aceptacion un evento")

# #node1.delete_account(user1)
# print('SHOW NOTIF JORDIPI')
# node1.show_notification(user1)
# print()
# print('SHOW NOTIF DIANECM')
# node1.show_notification(user2)
# print()
# print('SHOW NOTIF JORDIPI 1 AFTER DELETE NOTIF 1')
# node1.delete_notification(user1,1)
# node1.show_notification(user1)

node1.create_group(user1,'Mala Compannia', GType.Hierarchical, 'Esto no es nah')
node1.create_group(user2,'Buena Compannia', GType.Non_hierarchical)
node1.create_group(user1,'Media Compannia', GType.Non_hierarchical, 'Esto no es nah')
print()
print('SHOW GROUP JORDIPI CREATED')
# node1.show_group_belong_to(user1)

# node1.delete_group(user1,b'?\xe6\xc19\xa9m\xc7\xcd\xd8}\xa8\x95\xaf49\x92\xbf\x01\x1dF')
# node1.create_group(user1,'Mala Compannia', GType.Hierarchical, 'Esto no es nah')
# print()
# print('SHOW GROUP JORDIPI CREATED AFTER DELETE GROUP 1')
# node1.show_user_group_created(user1)

# print()
# print('SHOW GROUP DIANECM CREATED')
# node1.show_user_group_created(user2)

# node1.add_member_account(b'w\xd9NI\xbfi\xd9\x1f\xc4"\xf0\xa7\x91b\xe4\xd0\xfe\xff\xb0\xda',user2)
# node1.add_member_account(b'!.\x95\xe4\x9eO\xfbv\x12\x8f\xa4\xc4\r\xc5\x98\x02\x11\xf2\xafb',user2,"Capitan",15)
# node1.add_member_account(b'\xc9\x12\xab\xaf\xd7\x0fmB\xd3\x98l\xd9\x96\x8f\x03\x19X{h\xbc',user1)
# print()
# print('SHOW ALL GROUP JORDIPI BELONG')
# node1.show_user_in_group(user1)

# node1.create_event_personal(user1,'Boda de Primo','12/7/23-08:35','12/7/23-14:35')
# node1.create_event_personal(user1,'Cumple de Hermana','17/7/23-08:35','17/7/23-14:35')
# node1.create_event_personal(user1,'Evento Benefico','18/8/23-08:35','19/8/23-14:35')