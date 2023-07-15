from  utils import *
from constChord import *
import time 

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind(("127.0.0.1",5557))
receiver.listen()
ports = ["5123","5050",["5030"],["5132"]]
class User_Acccount:
    
    # def __init__(self,user_name):
    #     self.user_key = hash_key(user_name)

    def create_account(self,user_key,user_name,last_name,password):
        self.user_key = hash_key(user_key)
        data = {"message": CREATE_PROFILE, "ip":"127.0.0.1" , "port": "5557", "user_key": self.user_key ,
                "user_name": user_name , "last_name":last_name , "password":password  }
        address = ("127.0.0.1",int(ports[1]))
        print(f"Sending CREATE_PROFILE {self.user_key} request to 127.0.0.1:{ports[1]}")
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

p = User_Acccount()
#port = ports[0]
#p.create_account("Dano","Danilo","Perez","anymore")
#port = ports[1]
#p.create_account("Jordipynb","Jordan","Pla","lols")
#port = ports[2]
#p.create_account("La_Nanis","Dania","Mengana","1009")
#port = ports[3]
#p.create_account("Davi Zamoras","Luis David","Cruz","bruder")

#p.create_account("Por favor en otro rango","yeyo","lamoru","bruder")
#p.create_account("DianeCM","Dianelys","Cruz","bruder")
#p.create_account("Q'bola","luna","lamoru","bruder")
#p.create_account("Asere","yeyo","lamoru","bruder")
p.create_account("por fiiiinnn","Blau","lamoru","bruder")
p.create_account("Ultimo_intento","yeyo","lamoru","bruder")

p.create_account("Duke","Alma","lopez","bruder")

