import zmq
from constChord import *
from utils import *
import json
import random
import time 

#while True:
context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://127.0.0.1:5557")
    # send work
consumer_sender = context.socket(zmq.PUSH)
consumer_sender.connect("tcp://127.0.0.1:5123")
        
key = random.randint(915774693674738982705217759031541721583339531624,pow(2,160))
#Send a message to join to the network
data = {"message": LOOKUP_REQ, "ip":"127.0.0.1" , "port": "5557", "key": key }
#message = json.dumps(data).encode("utf-8")
print(f"Sending LOOKUP_REQ of {key} key")
consumer_sender.send_json(data)

time.sleep(10)

data = receiver.recv_json()
node = data["node"]
ip = data["ip"]
port = data["port"]
print(f"Recieving LOOKUP_REP of {node} for {key} key, from {ip}:{port}")
