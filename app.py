from  utils import *
from constChord import *
import time 
from database import Privacity, State, GType


ports = ["5123","5050","5030","5132"]

class Client:
    
    def __init__(self,my_address,server_addr):
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.bind(my_address)
        self.receiver.listen()
        self.server_addr = server_addr
        self.addr = my_address
   
    def recieve_data(self,request):
        conn, addr = self.receiver.accept()
        msg=conn.recv(1024)
        msg = msg.decode('utf-8')
        data =  json.loads(msg)
        response = data["message"]
        if not response  == str(int(request)+1):
            notify_data(f"Worg data response type expected {str(int(request)+1)} and got {response}","Error")
        else:
            return data
    
    def create_account(self, user_key, user_name, last_name, password,address=None):
        if not address: address = self.server_addr
        self.user_key = hash_key(user_key)
        data = {"message": CREATE_PROFILE, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "user_name": user_name, "last_name": last_name, "password": password  }
        print(f"Sending CREATE_PROFILE {self.user_key} request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)

    def get_account(self, user_key, password,address=None):
        self.user_key = hash_key(user_key)
        return self.check_account(self.user_key,address,password=password)
    
    def create_group(self, group_name, group_type,address=None):
        if not address: address = self.server_addr
        data = {"message": CREATE_GROUP, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "group_name": group_name, "group_type": group_type  }
        print(f"Sending CREATE_GROUP request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)

    def get_notifications(self,address=None):
        if not address: address = self.server_addr
        request = GET_NOTIFICATIONS
        data = {"message": request, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "sender_addr": self.addr  }
        print(f"Sending GET_NOTIFICATIONS request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)
        data = self.recieve_data(request) 
        return data['ids'], data['texts']

    def delete_notification(self, id_notification,address=None):
        if not address: address = self.server_addr
        data = {"message": DELETE_NOTIFICATION, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "id_notification": id_notification  }
        print(f"Sending DELETE_NOTIFICATION request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)

    def create_personal_event(self, event_name, date_initial, date_end, privacity=Privacity.Public.value, state=State.Personal.value, id_group=None, id_creator=None, address=None):
        if not address: address = self.server_addr
        data = {"message": CREATE_EVENT, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "event_name": event_name, 
                "date_initial": date_initial , "date_end": date_end, "visibility": privacity, "state": state, "group":id_group, "creator":id_creator  }
        print(f"Sending CREATE_EVENT request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)
    
    def get_all_events(self,address=None):
        if not address: address = self.server_addr
        request = GET_EVENTS
        data = {"message": request, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "sender_addr": self.addr  }
        print(f"Sending GET_EVENTS request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)
        data = self.recieve_data(request) 
        return data["ids_event"],data["event_names"],data["dates_ini"],data["dates_end"],data["states"],data["visibilities"],data["creators"],data["id_groups"]

    def get_groups_belong_to(self,address=None):
        if not address: address = self.server_addr
        request = GET_GROUPS
        data = {"message": request, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "sender_addr": self.addr  }
        print(f"Sending GET_GROUPS request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)
        data = self.recieve_data(request) 
        return data["ids_group"],data["group_names"],data["group_types"],data["group_refs"]
    
    def acept_pendient_event(self, id_event,address=None):
        if not address: address = self.server_addr
        data = {"message": ACEPT_EVENT, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "id_event": id_event  }
        print(f"Sending ACEPT_EVENT request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)

    def check_account(self,user_key,address,password = None):
        if not address: address = self.server_addr
        request = GET_PROFILE
        data = {"message": request, "ip": "127.0.0.1", "port": "5557", "user_key": user_key, "password": password, "sender_addr": self.addr  }
        print(f"Sending GET_PROFILE request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)
        data = self.recieve_data(request)       
        return data['user_name'], data['last_name']

    def delete_event(self, id_event,address=None):
        if not address: address = self.server_addr
        _,_,_,_,_,_,id_creator,id_group = self.get_event(self.user_key,id_event,address)
        assert id_creator == str(self.user_key)
        if id_group == None: self.delete_user_event(id_event,self.user_key,address)
        else:
            gtype = self.get_group_type(id_creator,id_group,address)
            if gtype == GType.Non_hierarchical.value: 
                ids_user,_ = self.get_inferior_members(id_creator,id_group,address)
                members = ids_user
            else: members = self.get_equal_members(id_creator,id_group,address)
            for id_user in members: self.delete_user_event(id_event,id_user,address)

    def delete_user_event(self,id_event,user_key,address):
        data = {"message":DELETE_EVENT, "ip":"127.0.0.1", "port":"5557", "user_key":user_key, "id_evet":id_event  }
        print(f"Sending DELETE_EVENT request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)

    def decline_pendient_event(self, id_event,address=None):
        if not address: address = self.server_addr
        _,_,_,_,state,_,id_creator,id_group = self.get_event(id_event,address)
        assert state == State.Pendient.value
        members = self.get_equal_members(id_creator,id_group,address)
        for id_user in members: self.delete_user_event(id_event,id_user,address)

    def create_groupal_event(self, event_name, date_initial, date_end, id_group, address=None):
        if not address: address = self.server_addr
        gtype = self.get_group_type(self.user_key,id_group,address)
        if gtype == GType.Hierarchical.value: 
            ids_user,_ = self.get_inferior_members(self.user_key,id_group,address)
            members = ids_user
        else: members = self.get_equal_members(self.user_key,id_group,address)
        for id_user in members: 
            if id_user == str(self.user_key): self.create_personal_event(event_name,date_initial,date_end,Privacity.Public.value,State.Asigned.value,id_group,str(self.user_key),address)
            elif gtype == GType.Non_hierarchical.value: self.create_personal_event(event_name,date_initial,date_end,Privacity.Public.value,State.Asigned.value,id_group,str(self.user_key),address)
            else: self.create_personal_event(event_name,date_initial,date_end,Privacity.Public.value,State.Pendient.value,id_group,str(self.user_key),address)

    def add_member(self, id_group, id_user, group_name, group_type, role=None, level=None,address=None):
        if not address: address = self.server_addr # EJUN GRUPO DEL QUE SE ES CREADOR
        user_name, last_name = self.check_account(id_user,address)
        if  user_name:
            self.add_member_group(id_group, id_user,role,level,address) #MEMBERGROUP
            self.add_member_account(id_user, id_group, group_name, group_type, str(self.user_key),address) #MEMBERACCOUNT

    def add_member_group(id_group, id_user,role,level,address=None):
        pass

    def add_member_account(id_user, id_group, group_name, group_type, ref,address=None):
        pass

    def get_event(self, id_event, address=None):
        if not address: address = self.server_addr
        request = GET_EVENT
        data = {"message": request, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "id_event": id_event, "sender_addr": self.addr  }
        print(f"Sending GET_EVENT request to {str(address)}")
        send_request(address,data=data)
        time.sleep(4)
        data = self.recieve_data(request) 
        return data["id_event"],data["event_name"],data["date_ini"],data["date_end"],data["states"],data["visibility"],data["creator"],data["id_group"]

    def get_group_type(self, id_creator, id_group,address=None):
        # IR A LA BASE DE DATOS DEL CREADOR DEL GRUPO
        # EN EL GRUPO SOLICITAR MIEMBROS INFERIORES AL ROL DEL USUARIO
        if not address: address = self.server_addr
        request = GET_HIERARCHICAL_MEMBERS
        pass

    def get_inferior_members(self, id_creator, id_group,address=None):
        # IR A LA BASE DE DATOS DEL CREADOR DEL GRUPO
        # EN EL GRUPO SOLICITAR MIEMBROS INFERIORES AL ROL DEL USUARIO
        if not address: address = self.server_addr
        request = GET_HIERARCHICAL_MEMBERS
        pass

    def get_equal_members(self, id_creator, id_group,address=None):
        # IR A LA BASE DE DATOS DEL CREADOR DEL GRUPO
        # EN EL GRUPO SOLICITAR MIEMBROS INFERIORES AL ROL DEL USUARIO
        if not address: address = self.server_addr
        request = GET_NON_HIERARCHICAL_MEMBERS
        pass
        
    def get_member_events(self, id_member,address=None):
        # SOLICITAR EVENTOS DEL MIEMBRO RESPETANDO SU PRIVACIDAD
        if not address: address = self.server_addr
        request = GET_EVENTS_MEMBER
        pass