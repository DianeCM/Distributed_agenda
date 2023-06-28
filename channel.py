import zmq
import random, math
from constChord import * 
from address import Address
import json
import hashlib

class Channel:

  def __init__(self,address,nBits=5):
    self.members = {}
    self.nBits = nBits
    self.MAXPROC = pow(2, nBits)
    self.address = address

  def join(self,address):
    newpid = random.choice(list(set([str(i) for i in range(self.MAXPROC)]) - set(self.members.keys())))
    self.members[newpid] = address
    print(f'Node {newpid} joined to chord, with address {address}')
    return newpid

  def exists(self,pid):
    return pid in self.members.keys()

  def leave(self,pid):
    assert pid in self.members.keys(), ''
    self.members.keys.remove(pid) 

  def hash_key(key: str) -> int:
    """
    Función de hash que calcula el hash SHA-1 de una cadena de caracteres y devuelve un número entero que se utiliza como la clave del nodo en la red Chord.
    """
    sha1 = hashlib.sha1(key.encode('utf-8'))
    hash_value = int(sha1.hexdigest(), 16) # convierte el hash SHA-1 en un número entero
    return hash_value

  
  def run(self):

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(str(self.address))

    message = socket.recv()
    data=json.loads(message.decode("utf-8"))
    message=data["message"]
    address = data["address"]
    print("Received request: %s" % message)

    if message == JOIN:
      data = {"nodeID": self.join(address), "nBits": self.nBits}
      message = json.dumps(data).encode("utf-8")
      socket.send(message)
      #socket.send_string(str(self.join(address)))        
