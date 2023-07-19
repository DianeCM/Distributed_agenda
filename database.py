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

    class Meta:
        database = None


class MemberAccount(Model):
    user = CharField(max_length=70,null=False)
    group = CharField(max_length=70,null=False)
    gname = CharField(max_length=50, null=False)
    gtype = CharField(max_length=15, null=False)
    ref = CharField(max_length=70,null=False)
    size = IntegerField(null=False)

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
    creator = CharField(max_length=70,null=True)
    group = CharField(max_length=70,null=True)
    size = IntegerField(null=False)
    
    class Meta:
        database = None
        primary_key = CompositeKey('user', 'event')


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
        try: 
            account = Account.create(user=userkeyn, name=name, last=last_name, passw=password)
            account.save()
        except IntegrityError:
            notify_data("Nombre de usuario ya existe","Error")
        

    def get_account(self, userkey: int, password: str):
        userkeyn = str(userkey)
        try: user = Account.get((Account.user == userkeyn) & (Account.passw == password)) if password else Account.get((Account.user == userkeyn)) 
        except DoesNotExist: 
            print("Usuario no existe")
            return None, None
        return user.name, user.last
    
    def create_group(self, userkey:int, id_group:str, name: str, gtype: str, size:int): 
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist: 
            print("Usuario no existe")
            return
        group = Group.create(creator=userkeyn, group=id_group, gname=name, gtype=gtype, size=size)
        group.save()
        self.add_member_account(userkey, group.group, name, gtype, userkeyn, size)
        self.add_member_group(group.group, userkey, "Propietario")
    
    def get_notifications(self, userkey: int):
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist: 
            print("Usuario no existe")
            return
        registers = Notification.select().where(Notification.user == userkeyn).order_by(Notification.notif.desc())
        ids_notif = []
        texts = []
        for register in registers:
            ids_notif.append(register.notif)
            texts.append(register.text)
        return ids_notif, texts
    
    def delete_notification(self, userkey: int, notif: str):
        userkeyn = str(userkey)
        try: notif = Notification.get((Notification.user == userkeyn) & (Notification.notif == notif))
        except DoesNotExist: 
            print("Notificación no existe")
            return
        notif.delete_instance(recursive=True)

    def create_event(self, userkey: int, id_event:str, name:str, date_ini:str, date_end:str, state:str, privacity:str, id_group:str, id_creator:str, size:int):
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist: 
            print("Usuario no existe")
            return
        registers = Event.select().where((Event.user == userkeyn) & (((date_ini <= Event.datec) & (Event.datec <= date_end)) | ((date_ini <= Event.datef) & (Event.datef <= date_end)) | ((Event.datec <= date_ini) & (date_ini <= Event.datef)) | ((Event.datec <= date_end) & (date_end <= Event.datef))))
        for register in registers:
            self.__add_notification(userkeyn, f"El evento {name} ({state}) tiene horarios coincidentes con el evento {register.ename} ({register.state})")
        event = Event.create(user=userkeyn, event=id_event, ename=name, datec=date_ini, datef=date_end, state=state, visib=privacity, group=id_group, creator=id_creator, size=size)
        event.save()
        if state == State.Pendient.value:
            self.__add_notification(userkey, f"Tiene un nuevo evento pendiente: {name}")

    def get_all_events(self, userkey: int, privacity:bool=False):
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist: 
            print("Usuario no existe")
            return
        if not privacity: registers = Event.select().where(Event.user == userkeyn)
        else: registers = Event.select().where((Event.user == userkeyn) & (Event.visib == Privacity.Public.value))
        idevent = []
        enames = []
        datesc = []
        datesf = []
        states = []
        visibs = []
        creators = []
        idgroups = []
        sizes = []
        for register in registers:
            idevent.append(register.event)
            enames.append(register.ename)
            datesc.append(register.datec)
            datesf.append(register.datef)
            states.append(register.state)
            visibs.append(register.visib)
            creators.append(register.creator)
            idgroups.append(register.group)
            sizes.append(register.size)
        return idevent, enames, datesc, datesf, states, visibs, creators, idgroups, sizes
    
    def get_event(self, userkey: int, id_event: str):
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist: 
            print("Usuario no existe")
            return
        event = Event.get((Event.user == userkeyn) & (Event.event == id_event))
        return event.event,event.ename,event.datec,event.datef,event.state,event.visib,event.creator,event.group,event.size
    
    def get_groups_belong_to(self, userkey: int):
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist: 
            print("Usuario no existe")
            return
        registers = MemberAccount.select().where(MemberAccount.user == userkeyn)
        idsgroup = []
        gnames = []
        gtypes = []
        refs = []
        sizes = []
        for register in registers:
            idsgroup.append(register.group)
            gnames.append(register.gname)
            gtypes.append(register.gtype)
            refs.append(register.ref)
            sizes.append(register.size)
        return idsgroup,gnames,gtypes,refs,sizes
    
    def accept_pendient_event(self, userkey: int, idevent: str):
        userkeyn = str(userkey)
        try: event = Event.get((Event.user==userkeyn) & (Event.event==idevent))
        except DoesNotExist: 
            print("Evento no existe")
            return
        event.state = State.Asigned.value
        event.save()
        self.__add_notification(userkey, f'Ha aceptado el evento {event.ename}')

    def get_inferior_members(self, userkey:str, idgroup:str):
        member = MemberGroup.get((MemberGroup.group==idgroup) & (MemberGroup.user==userkey))
        level = member.level
        registers = MemberGroup.select().where((MemberGroup.group==idgroup) & (MemberGroup.level > level))
        ids = []
        roles = []
        for register in registers:
            ids.append(register.user)
            roles.append(register.role)
        return ids, roles
    
    def get_equal_members(self, idgroup:str):
        registers = MemberGroup.select().where((MemberGroup.group==idgroup))
        ids = []
        for register in registers:
            ids.append(register.user)
        return ids
    
    def get_group_type(self, creatorkey:int, idgroup:str):
        creatorkeyn = str(creatorkey)
        try: Account.get(user=creatorkeyn)
        except DoesNotExist: 
            print("Usuario no existe")
            return
        group = Group.get((Group.group == idgroup) & (Group.creator == creatorkeyn))
        return group.gtype
    
    def delete_event(self, userkey:int, idevent:str):
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist: 
            print("Usuario no existe")
            return
        registers = Event.get((Event.event == idevent) & (Event.user == userkeyn))
        if registers: registers.delete_instance(recursive=True)
        else: print("Este evento no existe")
        
    def add_member_account(self, userkey:int, idgroup:str, gname:str, gtype:str, idref:str, size:int):
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist:
            print("Usuario no existe")
            return
        member = MemberAccount.create(user=userkeyn, group=idgroup, gname=gname, gtype=gtype, ref=idref, size=size)
        member.save()

    def add_member_group(self, idgroup: str, userkey: int, role: str=None, level: int=None):
        userkeyn = str(userkey)
        try: Group.get(group=idgroup)
        except DoesNotExist: return
        role_level = None
        if role == 'Propietario':
            try: role_level = MemberGroup.get((MemberGroup.group==idgroup)&(MemberGroup.role==role))
            except:
                asign = MemberGroup.create(group=idgroup, user=userkeyn, role=role, level=0)
                asign.save()
            if role_level is not None: print("Solo puede haber un propietario")
        elif role is None:
            asign = MemberGroup.create(group=idgroup, user=userkeyn, role="Miembro", level=1000)
            asign.save()
        else:
            try: role_level = MemberGroup.get((MemberGroup.group==idgroup)&(MemberGroup.role==role))
            except:
                if level is not None and 0 < level and level < 1000:
                    asign = MemberGroup.create(group=idgroup, user=userkeyn, role=role, level=level)
                    asign.save()
                else: print("Debe asignar un valor de nivel al rol mayor que 0 y menor que 1000")
                if role_level:
                    asign = MemberGroup.create(group=idgroup, iduser=userkeyn, role=role, level=role_level.level)
                    asign.save()

    def __add_notification(self, userkey: int, text: str):  
        userkeyn = str(userkey)
        try: Account.get(user=userkeyn)
        except DoesNotExist: return
        notif = Notification.create(user=userkeyn, text=text)
        notif.save()


    # PARA REPLICACION DE CHORD NO TOCAR
    def filter_function(self,condition,cls):
            def cond(row):
                key = row.user if not cls == Group else row.creator
                return condition(int(key))
            return cond 
    
    def get_filtered_db(self,condition,new_db_name):
        registers = {}
        for cls in self.classes:
            cls._meta.database = self.database
            registers[cls] = cls.select()


         # Crea una nueva base de datos
        conn_copia = SqliteDatabase(new_db_name)

        for cls in self.classes:
            cls._meta.database = conn_copia
            conn_copia.create_tables([cls])
            with conn_copia.atomic():
                for origen_row in registers[cls]:
                    if ((not (cls == Group)) and condition(origen_row.user)) or ((cls == Group) and condition(origen_row.creator)):
                        dest_row = cls.create(**origen_row.__dict__)
                        dest_row.save()
                        
        reg = Account.select()
        for r in reg:
            print(r.name)

        for cls in self.classes:
            cls._meta.database = self.database
    
        conn_copia.close()
       

    def replicate_db(self,db_name):
        registers ={}
        copy_db =  SqliteDatabase(db_name)
        for cls in self.classes:
            cls._meta.database = copy_db
            #if not copy_db.table_exists([cls]):
            #    notify_data("Aqquiiiiiiiiiiiiiii","Error")
            #    for cls in self.classes:
            #        cls._meta.database = self.database
            #    copy_db.close() 
            #    return False
            registers[cls] = cls.select()

        for cls in self.classes:
            cls._meta.database = self.database
            with self.database.atomic():
               try: 
                for row in registers[cls]:
                    try:
                        dest_row = cls.create(**row.__dict__)
                        dest_row.save()
                    except Exception:
                            cls.update(row.__dict__['__data__'])
                            notify_data("Aqquiiiiiiiiiiiiiii","Error")
               except : return False
        copy_db.close()
        return True

    def check_db(self):
        registers=[]
        for cls in self.classes:
            cls._meta.database = self.database
            registers.append(cls.select())

        notify_data("Accounts","GetData")
        for reg in registers[0]:
                print(reg.user,reg.name,reg.last,reg.passw)

        notify_data("Notifications","GetData")
        for reg in registers[1]:
                print(reg.user,reg.notif,reg.text)  

        notify_data("Groups","GetData")   
        for reg in registers[2]:
                print(reg.creator,reg.group,reg.gname,reg.gtype)

        notify_data("Member Account","GetData")      
        for reg in registers[3]:
                print(reg.user,reg.group,reg.ref)  

        notify_data("MemberGroup","GetData")    
        for reg in registers[4]:
                print(reg.group,reg.user,reg.role,reg.level) 

        notify_data("Events","GetData")  
        for reg in registers[5]:
                print(reg.user,reg.event,reg.ename,reg.datec,reg.datef,reg.state,reg.visib,reg.creator,reg.group)  

    def delete_replicated_db(self,condition):
        registers = {}
        for cls in self.classes:
            cls._meta.database = self.database
            registers = cls.select()
            for origen_row in registers:
                if ((not (cls == Group)) and condition(origen_row.user)) or ((cls == Group) and condition(origen_row.creator)):
                        origen_row.delete_instance()

        notify_data("Replicated data deleted.",'database')      
        notify_data("Current Data",'database')              
        reg = Account.select()
        for r in reg:
            print(r.name)
       
