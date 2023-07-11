import zmq
from constChord import *
from utils import *
import json
import random
import time 
import socket

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind(("127.0.0.1",5557))
receiver.listen()

ports = ["5132"]
a = [0,686916772571941171600637909103417451352519039489, 794143421378275501213700159784909595755571930874,
      865726554065021108825757911552689027386170761226, 915774693674738982705217759031541721583339531624,pow(2,160)]

#for i in range(len(a)-1):
#  for port in ports:
#    key = random.randint(a[i],a[i+1])
#    consumer_sender.connect(f"tcp://127.0.0.1:{port}")
#
#    print(f"Sending LOOKUP_REQ of {key} key to 127.0.0.1:{port}")
#    consumer_sender.send_json(data)
#
#    time.sleep(10)
#
#    data = receiver.recv_json()
#    node = data["node"]
#    ip = data["ip"]
#    port = data["port"]
#    print(f"Recieving LOOKUP_REP of {node} for {key} key, from {ip}:{port}")

pairs = []
for i in range(len(a)-1):
  for j,port in enumerate(ports):
    key = random.randint(a[i],a[i+1])
    value = random.randint(0,100)
    pairs.append((key,value,j))
    address = ("127.0.0.1",int(port))
    data = {"message": SET_DATA_REQ, "ip":"127.0.0.1" , "port": "5557", "key": key , "value": value}
    print(f"Sending SET_DATA_REQ of {key}:{value} key to 127.0.0.1:{port}")
    send_request(address,data,False)
    time.sleep(4)
    
def check_value(key,expected_value,port): 
    address = ("127.0.0.1",int(port))
    data = {"message": GET_DATA_REQ, "ip":"127.0.0.1" , "port": "5557", "key": key , "sender_addr": ("127.0.0.1",5557)}
    send_request(address,data,False)
    conn, addr = receiver.accept()
    msg=conn.recv(1024)
    msg = msg.decode('utf-8')
    data = json.loads(msg) 

    ip = data["ip"]
    port = data["port"]
    value = data["value"]
    print(f"Recieving GET_DATA_REP of {key}:{value}, from {ip}:{port}")
    assert  expected_value == value
    

def check_replication():
   for pair in pairs:
    key = pair[0]
    value = pair[1]
    port1 = ports[pair[2]]
    port2  = ports[(pair[2]+1)%len(ports)]
    check_value(key,value,port1)
    time.sleep(3)
    print()
    check_value(key,value,port2)
    time.sleep(3)
    print()

check_replication()
print("Successfull")

    



