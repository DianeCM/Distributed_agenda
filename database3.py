from peewee import *
# Cada vez que se vaya a eliminar algo, buscar en las replicaciones para que se eliminen tambien
# Caso no concebido pero que debemos tratar

class Account(Model):
    username = BigIntegerField(null=False, unique=True, primary_key=True)
    name = CharField(max_length=15, null=False)
    last_name = CharField(max_length=40, null=False)

    class Meta:
        database = None


class Account_Notifications(Model):
    username = ForeignKeyField(Account, on_delete='CASCADE')
    id_notif = IntegerField(null=True)
    notification = CharField(max_length=300)

    class Meta:
        database = None
        primary_key = CompositeKey('username', 'id_notif')
        autoincremental = 1

    def save(self, *args, **kwargs):
        if not self.id_notif:
            self.id_notif = Account_Notifications._meta.autoincremental
            Account_Notifications._meta.autoincremental += 1
        Model.save(self, *args, **kwargs)


class Group(Model):
    gname = CharField(max_length=50, null=False, unique=True, primary_key=True)
    gtype = CharField(max_length=15, null=False)
    description = CharField(max_length=100, null=True)
    propietary = ForeignKeyField(Account, on_delete='CASCADE')

    class Meta:
        database = None


class Account_Groups(Model):
    username = ForeignKeyField(Account, on_delete='CASCADE')
    gname = ForeignKeyField(Group, on_delete='CASCADE')
    role = CharField(max_length=50, null=False)
    priority = IntegerField(null=False)

    class Meta:
        database = None
        primary_key = CompositeKey('username', 'gname')


class Events(Model):
    username = ForeignKeyField(Account, on_delete='CASCADE')
    id_event = IntegerField(null=True)
    ename = CharField(max_length=100, null=False)
    date_ini = DateTimeField(null=False)
    date_end = DateTimeField(null=False)
    state = CharField(max_length=9, null=False)
    visibility = CharField(max_length=9, null=False)

    class Meta:
        database = None
        primary_key = CompositeKey('username', 'id_event')
        autoincremental = 1

    def save(self, *args, **kwargs):
        if not self.id_event:
            self.id_event = Events._meta.autoincremental
            Events._meta.autoincremental += 1
        Model.save(self, *args, **kwargs)


class NodeYumi:
    def __init__(self, id: int):
        self.id = id
        self.db_name = f"{self.id}.db"
        self.database = SqliteDatabase(self.db_name)

    def create_account(self, name: str, last_name: str):
        Account._meta.database = self.database
        if not Account.table_exists():
            self.database.create_tables([Account])
        account = Account.create(
            username=self.id, name=name, last_name=last_name)
        account.save()
        return account

    def delete_account(self):
        for cls in [Account, Account_Notifications, Group, Account_Groups, Events]:
            cls._meta.database = self.database
        if not Account.table_exists():
            self.database.create_tables([Account])
        account = Account.get(username=self.id)
        account.delete_instance(recursive=True)

    def merge_client_information(self, other):
        pass ################ MERGE ########################################################

    def add_notification(self, notification: str):
        Account_Notifications._meta.database = self.database
        Account._meta.database = self.database
        if not Account_Notifications.table_exists():
            self.database.create_tables([Account_Notifications])
        account = Account.get(username=self.id)
        notif = Account_Notifications.create(
            username=account, notification=notification)
        notif.save()

    def show_notification(self):
        Account_Notifications._meta.database = self.database
        if not Account_Notifications.table_exists():
            self.database.create_tables([Account_Notifications])
        registers = Account_Notifications.select().where(Account_Notifications.username ==
                                                         self.id).order_by(Account_Notifications.id_notif.desc())
        for register in registers:
            print(register.id_notif, register.notification)

    def remove_notification(self, id_notif: int):
        for cls in [Account, Account_Notifications, Group, Account_Groups, Events]:
            cls._meta.database = self.database
        if not Account_Notifications.table_exists():
            self.database.create_tables([Account_Notifications])
        notif = Account_Notifications.get((Account_Notifications.username == self.id) & (
            Account_Notifications.id_notif == id_notif))
        notif.delete_instance(recursive=True)

    def create_group():
        pass

    def modify_group():
        pass
    
    def delete_group():
        pass

    def add_member_to_group():
        pass

    def remove_member_from_group():
        pass

    def add_events():
        pass

    def delete_event():
        pass

    def acept_event():
        pass

    def decline_event():
        pass

    def change_events():
        pass

    # QUERIES

# TEST CASE
node1 = NodeYumi(1234)
account1 = node1.create_account("Jordan", "Pla Gonzalez")

node2 = NodeYumi(2345)
account2 = node2.create_account("Dianelys", "Cruz Mengana")

node1.add_notification("Tienes un evento que colisiona")
node1.add_notification("Tienes pendiente de aceptacion un evento")
node2.add_notification("Tienes un evento que colisiona")
node2.add_notification("Tienes pendiente de aceptacion un evento")

print('SHOW NOTIF NODE 1')
node1.show_notification()
node1.remove_notification(1)
print()
print('SHOW NOTIF NODE 1 AFTER DELETE NOTIF 1')
node1.show_notification()
print()
print('SHOW NOTIF NODE 2')
node2.show_notification()
print()
print('SHOW ALL NOTIF DATABASE 1234')
Account_Notifications._meta.database = SqliteDatabase('1234.db')
result = Account_Notifications.select()
for res in result:
    print(res.id_notif, res.notification)

print()
print('CREATE GROUP BY NODE 1')


group1 = Group.create(gname='Mala Compannia', gtype='Jerarquico',
                      description='Esto no es nah', propietary=account1)
group1.save()
group2 = Group.create(gname='Buena Compannia', gtype='No Jerarquico',
                      description='Esto no es nah', propietary=account2)
group2.save()

asign1 = Account_Groups.create(
    username=account1, gname=group1, role='Propietario', priority=0)
asign1.save()
asign2 = Account_Groups.create(
    username=account2, gname=group1, role='Miembro', priority=1000000)
asign2.save()
asign3 = Account_Groups.create(
    username=account2, gname=group2, role='Propietario', priority=0)
asign3.save()
asign4 = Account_Groups.create(
    username=account1, gname=group2, role='Miembro', priority=1000000)
asign4.save()

event1 = Events.create(username=account1, ename='Boda de Primo', date_ini='12/7/23-08:35',
                                date_end='12/7/23-14:35', state='Pendiente', visibility='Publico')
event1.save()
event2 = Events.create(username=account1, ename='Cumple de Hermana',
                                date_ini='17/7/23-08:35', date_end='17/7/23-14:35', state='Pendiente', visibility='Publico')
event2.save()
event3 = Events.create(username=account1, ename='Evento Benefico', date_ini='18/8/23-08:35',
                                date_end='19/8/23-14:35', state='Pendiente', visibility='Publico')
event3.save()
event4 = Events.create(username=account2, ename='Boda de Primo', date_ini='12/7/23-08:35',
                                date_end='12/7/23-14:35', state='Pendiente', visibility='Publico')
event4.save()
event5 = Events.create(username=account2, ename='Cumple de Hermana',
                                date_ini='17/7/23-08:35', date_end='17/7/23-14:35', state='Pendiente', visibility='Publico')
event5.save()
event6 = Events.create(username=account2, ename='Evento Benefico', date_ini='18/8/23-08:35',
                                date_end='19/8/23-14:35', state='Pendiente', visibility='Publico')
event6.save()

result = Account.filter(Account.username == 1234)
for res in result:
    print(res.name, res.last_name)
result = Group.filter(Group.propietary == 1234)
for res in result:
    print(res.gname, res.gtype)
result = Account_Notifications.filter(Account_Notifications.username == 1234)
for res in result:
    print(res.id_notif, res.notification)
result = Account_Groups.filter(Account_Groups.username == 1234)
for res in result:
    print(res)
result = Events.filter(Events.username == 1234)
for res in result:
    print(res.ename, res.state)


account1 = Account.get(username=1234)
print(account1)
account1.delete_instance(recursive=True)

result = Account.select()
for res in result:
    print(res.name, res.last_name)
result = Group.select()
for res in result:
    print(res.gname, res.gtype, res.propietary)
result = Account_Notifications.select()
for res in result:
    print(res.id_notif, res.notification)
result = Account_Groups.select()
for res in result:
    print(res)
result = Events.select()
for res in result:
    print(res)
