from  utils import *
from constChord import *
import time 

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind(("127.0.0.1",5557))
receiver.listen()
ports = ["5030"]
class User_Acccount:
    
    def __init__(self,user_name):
        self.user_key = hash_key(user_name)

    def create_account(self,user_name,last_name,password):
        data = {"message": CREATE_PROFILE, "ip":"127.0.0.1" , "port": "5557", "hash_key": self.user_key ,"user_name": user_name , "last_name":last_name , "password":password  }
        address = ("127.0.0.1",int(ports[0]))
        print(f"Sending CREATE_PROFILE request to 127.0.0.1:{ports[0]}")
        send_request(address,data,False)
        time.sleep(4)

    def get_confirmed_eventes(self):
        pass
    def get_pendient_eventes(self):
        pass

    def get_user_eventes(self,user_key,date_time):
        pass

