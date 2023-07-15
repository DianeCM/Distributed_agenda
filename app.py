from  utils import *
from constChord import *
import time 
from database import Privacity, State, GType

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind(("127.0.0.1",5557))
receiver.listen()
ports = ["5123"]
class User_Acccount:

    def create_account(self, user_key, user_name, last_name, password):
        self.user_key = hash_key(user_key)
        data = {"message":CREATE_PROFILE, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key,
                "user_name":user_name , "last_name":last_name , "password":password  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending CREATE_PROFILE request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

    def get_account(self, user_key, password):
        self.user_key = user_key
        data = {"message":GET_PROFILE, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "password":password  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending GET_PROFILE request to 127.0.0.1:{ports[0]}")
        data = send_request(address,data,True,False)
        time.sleep(4)
        return data['user_name'] if data else None, data['last_name'] if data else None

    def delete_account(self):
        data = {"message":DELETE_PROFILE, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending DELETE_PROFILE request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

    def create_personal_event(self, event_name, date_initial, date_end, privacity):
        data = {"message":CREATE_PEVENT, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "event_name":event_name,
                "date_initial":date_initial , "date_end":date_end, "visibility":privacity, "creator":self.user_key  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending CREATE_PEVENT request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

    def create_group(self, group_name, group_type, group_description):
        data = {"message":CREATE_GROUP, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key,
                "group_name":group_name , "group_type":group_type, "group_description":group_description  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending CREATE_GROUP request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

    def get_notifications(self):
        data = {"message":GET_NOTIFICATIONS, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending GET_NOTIFICATIONS request to 127.0.0.1:{ports[0]}")
        data = send_request(address,data,True,False)
        time.sleep(4)
        return data['ids'] if data else None, data['text'] if data else None

    def delete_notification(self, id_notification):
        data = {"message":DELETE_NOTIFICATION, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "id_notification":id_notification  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending DELETE_NOTIFICATION request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

    def get_all_events(self):
        data = {"message":GET_EVENTS, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending GET_EVENTS request to 127.0.0.1:{ports[0]}")
        data = send_request(address,data,True,False)
        time.sleep(4)
        return data["ids"], data["name"], data["date_ini"], data["data_end"], data["state"], data["creator"]

    def delete_event(self, id_event):
        data = {"message":DELETE_EVENT, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "id_evet":id_event  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending DELETE_EVENT request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

    def acept_pendient_event(self, id_event):
        data = {"message":ACEPT_EVENT, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "id_evet":id_event  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending ACEPT_EVENT request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

    def decline_pendient_event(self, id_event):
        data = {"message":DECLINE_EVENT, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "id_evet":id_event  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending DECLINE_EVENT request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

    def get_groups_belong_to(self):
        # DEVOLVER LA LISTA DE GRUPOS A LOS QUE PERTENECE (ID, NOMBRE, TIPO)
        pass

    def create_groupal_event(self, id_group, event_name, date_initial, date_end, privacity):
        data = {"message":CREATE_GEVENT, "ip":"127.0.0.1", "port":"5557", "user_key":self.user_key, "event_name":event_name,
                "date_initial":date_initial , "date_end":date_end, "visibility":privacity, "creator":self.user_key, "id_group":id_group  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending CREATE_PEVENT request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

    def add_member_to_group(self, id_group, id_user):
        # AQUI HAY QUE PONERLO EN EL GRUPO DEL CREADOR (QUE ES EL USUARIO)
        # AQUI HAY QUE PONERLO EN LA DATABASE DEL MIEMBRO QUE PERTENECE A ESTE GRUPO
        pass

    def get_inferior_members(self, id_creator, id_group):
        # IR A LA BASE DE DATOS DEL CREADOR DEL GRUPO
        # EN EL GRUPO SOLICITAR MIEMBROS INFERIORES AL ROL DEL USUARIO
        pass

    def get_member_events(self, id_member):
        # SOLICITAR EVENTOS DEL MIEMBRO RESPETANDO SU PRIVACIDAD
        pass