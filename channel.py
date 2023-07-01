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

  def join(self,ip,port):
    address = Address(ip,port)
    newpid = hash_key(str(address))  ##cambiar por el ip !!!!!!!!!!!!!!!!!!!!
    self.nodes_ID.append(newpid)
    self.nodes_ID.sort
    self.members[newpid] = address
    print(f'Node {newpid} joined to chord, with address {str(address)}')
    return newpid

  def exists(self,pid):
    return pid in self.members.keys()

  def leave(self,pid):
    assert pid in self.members.keys(), ''
    self.members.keys.remove(pid) 

  
  def run(self):

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(str(self.address))

    while True:
      message = socket.recv()
      data=json.loads(message.decode("utf-8"))
      message=data["message"]
      ip = data["ip"]
      port = data["port"]
      print("Received request: %s" % message)

      if message == JOIN:
        new_id = self.join(ip,port)
        nodes_address= [ (self.members[id].ip,self.members[id].port) for id in self.nodes_ID ]
        
        data = {"nodeID": new_id, "nBits": self.nBits,"nodes_ID":self.nodes_ID,"addresses": nodes_address}
        message = json.dumps(data).encode("utf-8")
        socket.send(message)
        #socket.send_string(str(self.join(address)))