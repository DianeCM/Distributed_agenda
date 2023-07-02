import zmq
from constChord import *
from utils import *
import json
import random
while True:
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    #self.socket.bind(str(self.address))
    socket.connect(str(Address("localhost","5555")))
        
    key = random.randint(0,pow(2,159))
    #Send a message to join to the network
    data = {"message": LOOKUP_REQ, "ip":"localhost" , "port": "5555", "key": key }
    message = json.dumps(data).encode("utf-8")
    socket.send(message)
