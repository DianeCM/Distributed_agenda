import zmq
import random, math
from constChord import * 
import json
from utils import *


class Channel:

  def __init__(self,address:Address,nBits=160):
    self.members = {}
    self.nBits = nBits
    self.MAXPROC = pow(2, nBits)
    self.address = address
    self.nodes_ID=[]

    #initializing sockets
    context = zmq.Context()
    # recieve work
    self.receiver = context.socket(zmq.PULL)
    self.receiver.bind(str(self.address))

  def join(self,ip,port):
    address = Address(ip,port)
    newpid = hash_key(str(address))  ##cambiar por el ip !!!!!!!!!!!!!!!!!!!!
    self.nodes_ID.append(newpid)
    self.nodes_ID.sort()
    self.members[newpid] = address
    print(f'Node {newpid} joined to chord, with address {str(address)}')
    return newpid

  def exists(self,pid):
    return pid in self.members.keys()

  def leave(self,pid):
    assert pid in self.members.keys(), ''
    self.members.keys.remove(pid) 

  def lookup_key(self,key):
      while True:
        print("hallo") 
        if len(self.nodes_ID) > 0:
            node = random.choice(self.nodes_ID)
            context = zmq.Context()
            socket = context.socket(zmq.PUSH)
            #self.socket.bind(str(self.address))
            socket.connect(self.members[node])
        
            #Send a message to join to the network
            print("Sending Look up key request")
            data = {"message": LOOKUP_REQ, "ip": self.address.ip , "port": self.address.port , "key":key}
            message = json.dumps(data).encode("utf-8")
            socket.send(message)

  def run(self):

    while True:

      #getting request
      data = self.receiver.recv_json()
      #data=json.loads(message.decode("utf-8"))

      #unpacking data 
      message=data["message"]
      ip = data["ip"]
      port = data["port"]
      print("Received request: %s" % message)
      
      #answer request
      if message == JOIN:

        # getting new node id 
        new_id = self.join(ip,port)
        nodes_address= [ (self.members[id].ip,self.members[id].port) for id in self.nodes_ID ]
        print(self.nodes_ID)

        #load message
        data = {"nodeID": new_id, "nBits": self.nBits,"nodes_ID":self.nodes_ID,"addresses": nodes_address}
        
        #Sending reply

        context = zmq.Context()
        consumer_sender = context.socket(zmq.PUSH)
        consumer_sender.connect(f"tcp://{ip}:{port}")
        consumer_sender.send_json(data)
        consumer_sender.close()

      if message == LOOKUP_REQ and len(self.nodes_ID) > 0:
        key = data["key"]
        #node = random.choice(self.nodes_ID)
        node = self.nodes_ID[-1]
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.connect(str(self.members[node]))
       
        #Send lookup request
        print("Sending Look up key request")
        data = {"message": LOOKUP_REQ, "ip": self.address.ip , "port": self.address.port , "key":key}
        socket.send_json(data)
        socket.close()

      if message == LOOKUP_REP:
          node = data["node"]
          key = data["key"]
          print(f'Node {node} contains the key {key}')

    