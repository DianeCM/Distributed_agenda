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
        send_request(address,data,False,False)
        time.sleep(4)

    def get_account(self, user_key, password,address=None):
        if not address: address = self.server_addr
        self.user_key = hash_key(user_key)
        request = GET_PROFILE
        data = {"message": request, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "password": password, "sender_addr": self.addr  }
        print(f"Sending GET_PROFILE request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)
        data = self.recieve_data(request)       
        return data['user_name'], data['last_name']
    
    def create_group(self, group_name, group_type,address=None):
        if not address: address = self.server_addr
        data = {"message": CREATE_GROUP, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "group_name": group_name, "group_type": group_type  }
        print(f"Sending CREATE_GROUP request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)

    def get_notifications(self,address=None):
        if not address: address = self.server_addr
        request = GET_NOTIFICATIONS
        data = {"message": request, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "sender_addr": self.addr  }
        print(f"Sending GET_NOTIFICATIONS request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)
        data = self.recieve_data(request) 
        return data['ids'], data['texts']

    def delete_notification(self, id_notification,address=None):
        if not address: address = self.server_addr
        data = {"message": DELETE_NOTIFICATION, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "id_notification": id_notification  }
        print(f"Sending DELETE_NOTIFICATION request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)

    def create_personal_event(self, event_name, date_initial, date_end, privacity,address=None):
        if not address: address = self.server_addr
        data = {"message": CREATE_PEVENT, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "event_name": event_name, "date_initial": date_initial , "date_end": date_end, "visibility": privacity  }
        print(f"Sending CREATE_PEVENT request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)
    
    def get_all_events(self,address=None):
        if not address: address = self.server_addr
        request = GET_EVENTS
        data = {"message": request, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "sender_addr": self.addr  }
        print(f"Sending GET_EVENTS request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)
        data = self.recieve_data(request) 
        return data["ids_event"],data["event_names"],data["dates_ini"],data["dates_end"],data["states"],data["visibilities"],data["creators"],data["id_groups"]

    def get_groups_belong_to(self,address=None):
        if not address: address = self.server_addr
        request = GET_GROUPS
        data = {"message": request, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "sender_addr": self.addr  }
        print(f"Sending GET_GROUPS request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)
        data = self.recieve_data(request) 
        return data["ids_group"],data["group_names"],data["group_types"],data["group_refs"]
    
    def acept_pendient_event(self, id_event,address=None):
        if not address: address = self.server_addr
        data = {"message": ACEPT_EVENT, "ip": "127.0.0.1", "port": "5557", "user_key": self.user_key, "id_event": id_event  }
        print(f"Sending ACEPT_EVENT request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)




    


    # PENDIENTES A ARREGLAR (NO ESPERES QUE SIRVAN AUN) ********************************************************************
    # ESTO ES UN DILEMON
    def delete_event(self, id_event,address=None):
        # SI ES PERSONAL SE ELIMINA Y NO HAY PROBLEMA, PERO SI ES CREADOR DE EVENTO GRUPAL HAY UN PROBLEMON GORDO
        # IR AL GRUPO EN DONDE FUE CREADO
        # SI ES JERARQUICO, HAY QUE ELIMINARLO PARA TODOS LOS JERARQUICAMENTE INFERIOR
        # SI NO ES JERARQUICO, HAY QUE ELIMINARLO PARA TODOS LOS MIEMBROS DEL GRUPO
        # LO QUE IMPLICA PREGUNTAR POR TODOS ESO ID EN LA RED CHORD
        if not address: address = self.server_addr
        data = {"message":DELETE_EVENT, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "id_evet":id_event  }
        print(f"Sending DELETE_EVENT request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)

    def decline_pendient_event(self, id_event,address=None):
        # AQUI EL SISTEMA SOLO VA A PERMITIR LLEGAR SI ES UN EVENTO DE GRUPO NO JERARQUICO
        # SE ELIMINA DE ÉL Y SE VA AL GRUPO DONDE FUE CREADO
        # PARA TODOS LOS MIEMBROS DEL GRUPO SE ELIMINA EL EVENTO (NOTIFICAR QUE EL EVENTO FUE RECHAZADO)
        if not address: address = self.server_addr
        request = DECLINE_EVENT
        pass

    def create_groupal_event(self, address=None):
        # SE CREA EL EVENTO EN EL USUARIO REFERENCIANDO AL GRUPO Y A EL COMO CREADO
        # IR AL GRUPO EN DONDE FUE CREADO
        # SI ES JERARQUICO, HAY QUE ASIGNARLO PARA TODOS LOS JERARQUICAMENTE INFERIOR
        # SI NO ES JERARQUICO, HAY QUE ASIGNARLO PARA TODOS LOS MIEMBROS DEL GRUPO EN PENDIENTE
        # LO QUE IMPLICA PREGUNTAR POR TODOS ESO ID EN LA RED CHORD
        if not address: address = self.server_addr
        request = CREATE_GEVENT
        pass

    def add_member_to_group(self, id_group, id_user,address=None):
        # COMPROBAR QUE EL ID DE MIEMBRO EXISTE
        # PONERLO EN EL MEMBER_GROUP DEL CREADOR (QUE ES EL USUARIO)
        # PONERLO EN LA MEMBER_ACCOUNT DEL MIEMBRO
        if not address: address = self.server_addr
        request = ADD_MEMBER
        pass

    def get_inferior_members(self, id_creator, id_group,address=None):
        # IR A LA BASE DE DATOS DEL CREADOR DEL GRUPO
        # EN EL GRUPO SOLICITAR MIEMBROS INFERIORES AL ROL DEL USUARIO
        if not address: address = self.server_addr
        request = GET_HIERARCHICAL_MEMBERS
        pass
        
    def get_member_events(self, id_member,address=None):
        # SOLICITAR EVENTOS DEL MIEMBRO RESPETANDO SU PRIVACIDAD
        if not address: address = self.server_addr
        request = GET_EVENTS_MEMBER
        pass