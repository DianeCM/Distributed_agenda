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
   
    def recieve_data(self,request):   # ESTO ES LO QUE HABLAMOS QUE IBAS A CORREGIR PORQUE NO USAS LOS REQUEST
        conn, addr = self.receiver.accept()
        msg=conn.recv(1024)
        msg = msg.decode('utf-8')
        data =  json.loads(msg)
        response = data["message"]
        if not response  == str(int(GET_PROFILE)+1):
            notify_data(f"Worg data response type expected {str(int(GET_PROFILE)+1)} and got {response}","Error")
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
        return data["ids_event"],data["event_names"],data["dates_ini"],data["datas_end"],data["states"],data["visibilities"],data["creators"],data["id_groups"]


    
    


    # PENDIENTES A ARREGLAR (NO ESPERES QUE SIRVAN AUN) ********************************************************************
    # ESTO ES UN DILEMON
    def delete_event(self, id_event,address=None):
        data = {"message":DELETE_EVENT, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "id_evet":id_event  }
        if not address: address = self.server_addr
        print(f"Sending DELETE_EVENT request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)

    def acept_pendient_event(self, id_event,address=None):
        data = {"message":ACEPT_EVENT, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "id_evet":id_event  }
        if not address: address = self.server_addr
        print(f"Sending ACEPT_EVENT request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)

    def decline_pendient_event(self, id_event,address=None):
        data = {"message":DECLINE_EVENT, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "id_evet":id_event  }
        if not address: address = self.server_addr
        print(f"Sending DECLINE_EVENT request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)

    def get_groups_belong_to(self,address=None):
        # DEVOLVER LA LISTA DE GRUPOS A LOS QUE PERTENECE (ID, NOMBRE, TIPO)
        pass

    def create_groupal_event(self, id_group, event_name, date_initial, date_end, privacity,address=None):
        data = {"message":CREATE_GEVENT, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "event_name":event_name,
                "date_initial":date_initial , "date_end":date_end, "visibility":privacity, "creator":self.user_key, "id_group":id_group  }
        if not address: address = self.server_addr
        print(f"Sending CREATE_PEVENT request to {str(address)}")
        send_request(address,data,False,False)
        time.sleep(4)

    def add_member_to_group(self, id_group, id_user,address=None):
        # AQUI HAY QUE PONERLO EN EL GRUPO DEL CREADOR (QUE ES EL USUARIO)
        # AQUI HAY QUE PONERLO EN LA DATABASE DEL MIEMBRO QUE PERTENECE A ESTE GRUPO
        pass

    def get_inferior_members(self, id_creator, id_group,address=None):
        # IR A LA BASE DE DATOS DEL CREADOR DEL GRUPO
        # EN EL GRUPO SOLICITAR MIEMBROS INFERIORES AL ROL DEL USUARIO
        pass
    def get_member_events(self, id_member,address=None):
        # SOLICITAR EVENTOS DEL MIEMBRO RESPETANDO SU PRIVACIDAD
        pass