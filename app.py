from  utils import *
from constChord import *
import time 

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind(("127.0.0.1",5557))
receiver.listen()
ports = ["5123"]
class User_Acccount:
    
    # def __init__(self,user_name):
    #     self.user_key = hash_key(user_name)

    def create_account(self,user_key,user_name,last_name,password):
        self.user_key = hash_key(user_key)
        data = {"message": CREATE_PROFILE, "ip":"127.0.0.1" , "port": "5557", "user_key": self.user_key ,
                "user_name": user_name , "last_name":last_name , "password":password  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending CREATE_PROFILE {self.user_key} request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

# ESTO ES LO QUE AGREGUE POR SI LUEGO NO SIRVE PANAS
    def get_account(self,user_key,password):
        self.user_key = user_key
        data = {"message": GET_PROFILE, "ip":"127.0.0.1" , "port": "5557", "user_key": self.user_key , "password":password  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending GET_PROFILE request to 127.0.0.1:{ports[0]}")
        data = send_request(address,data,True,False)
        time.sleep(4)
        return data['user_name'], data['last_name']
    
    def create_group(self,group_name,group_type,group_description):
        data = {"message": CREATE_GROUP, "ip":"127.0.0.1" , "port": "5557", "user_key":self.user_key,
                "group_name": group_name ,"group_type": group_type , "group_description":group_description }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending CREATE_GROUP request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False,False)
        time.sleep(4)

    def get_confirmed_eventes(self):
        pass
    def get_pendient_eventes(self):
        pass

    def get_user_eventes(self,user_key,date_time):
        pass

p = User_Acccount("Danilo")
p.create_account("Danilo","Perez","anymore")
