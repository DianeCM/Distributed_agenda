import zmq
import channel #-
import random, math #-
from constChord import * #-
from address import Address

class ChordNode:
    def __init__(self,chan_address,address):
        self.address=address
        self.chan_address = chan_address
        

    def run(self):
        print("Connecting to Channel Server")
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        #self.socket.bind(str(self.address))
        self.socket.connect(str(self.chan_address))
        print("Sending Message")
        self.socket.send_string(JOIN)
        #  Get the reply.
        message = self.socket.recv().decode()
        print("Joined to the channel as node %s" % (message))

node= ChordNode(Address("localhost","5555"),Address("localhost","5000"))
node.run()