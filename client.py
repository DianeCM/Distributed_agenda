import zmq
from constChord import *
from utils import *
import json
import random

#while True:
context = zmq.Context()
consumer_receiver = context.socket(zmq.PULL)
consumer_receiver.bind("tcp://127.0.0.1:5557")
    # send work
consumer_sender = context.socket(zmq.PUSH)
consumer_sender.connect("tcp://127.0.0.1:5555")
        
key = random.randint(0,pow(2,159))
#Send a message to join to the network
data = {"message": LOOKUP_REQ, "ip":"localhost" , "port": "5555", "key": key }
#message = json.dumps(data).encode("utf-8")
consumer_sender.send_json(data)
