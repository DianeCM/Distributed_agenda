import zmq
import random, math
from constChord import * 
from address import Address

class Channel:

  def __init__(self,address,nBits=5):
    self.members = {}
    self.nBits = nBits
    self.MAXPROC = pow(2, nBits)
    self.address = address

  def join(self):
    newpid = random.choice(list(set([str(i) for i in range(self.MAXPROC)]) - set(self.members.keys())))
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
    message = socket.recv().decode()
    print("Received request: %s" % message)
    if message == JOIN:
      socket.send_string(str(self.join()))        
