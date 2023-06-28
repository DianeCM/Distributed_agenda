import zmq
import channel #-
import random, math #-
from constChord import * #-
from address import Address
import json 
class ChordNode:

    def __init__(self,chan_address,address):
        self.address=address
        self.chan_address = chan_address
        self.nodeSet = []                           # Nodes discovered so far
        self.nodeID = None
        self.nBits = None
        self.FT = None
        self.node_address = {}
    
    #ok
    def inbetween(self, key, lwb, upb):                                         
        if lwb <= upb:                                                            
            return lwb <= key < upb                                                                                                         
        return (lwb <= key and key < upb + self.MAXPROC) or (lwb <= key + self.MAXPROC and key < upb)                        
    
    def addNode(self, nodeID):                                                  
        self.nodeSet.append(int(nodeID))                                         
        self.nodeSet = list(set(self.nodeSet))                                    
        self.nodeSet.sort()         

    def delNode(self, nodeID):                                                  
        assert nodeID in self.nodeSet, ''                                         
        del self.nodeSet[self.nodeSet.index(nodeID)]                              
        self.nodeSet.sort() 

    def finger(self, i):
        succ = (self.nodeID + pow(2, i-1)) % self.MAXPROC    # succ(p+2^(i-1))
        lwbi = self.nodeSet.index(self.nodeID)               # own index in nodeset
        upbi = (lwbi + 1) % len(self.nodeSet)                # index next neighbor
        for k in range(len(self.nodeSet)):                   # go through all segments
            if self.inbetween(succ, self.nodeSet[lwbi]+1, self.nodeSet[upbi]+1):
                return self.nodeSet[upbi]                        # found successor
            (lwbi,upbi) = (upbi, (upbi+1) % len(self.nodeSet)) # go to next segment
        return None                                                                

    def recomputeFingerTable(self):
        self.FT[0]  = self.nodeSet[self.nodeSet.index(self.nodeID)-1] # Predecessor
        self.FT[1:] = [self.finger(i) for i in range(1,self.nBits+1)] # Successors

    #ok
    def localSuccNode(self, key): 
        if self.inbetween(key, self.FT[0]+1, self.nodeID+1): # key in (FT[0],self]
            return self.nodeID                                 # node is responsible
        elif self.inbetween(key, self.nodeID+1, self.FT[1]): # key in (self,FT[1]]
            return self.FT[1]                                  # successor responsible
        for i in range(1, self.nBits+1):                     # go through rest of FT
            if self.inbetween(key, self.FT[i], self.FT[(i+1) % self.nBits]):
                return self.FT[i]                                # key in [FT[i],FT[i+1])
    
    #ok
    def run(self):
        print("Connecting to Channel Server")
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        #self.socket.bind(str(self.address))
        socket.connect(str(self.chan_address))
        
        #Send a message to join to the network
        print("Sending Message")
        data = {"message": JOIN, "address": str(self.address)}
        message = json.dumps(data).encode("utf-8")
        socket.send(message)

        #  Get the reply.
        message = socket.recv()
        data=json.loads(message.decode("utf-8"))
        nodeID=data["nodeID"]
        nBits = data["nBits"]
        print("Joined to an %s chord network as node %s" % (nBits,nodeID))
        self.nodeID = nodeID 
        self.nBits = nBits
        self.FT = [None for i in range(self.nBits+1)] # FT[0] is predecessor #-

        #Receiving requests
        while True:
            message = socket.recv()
            data=json.loads(message.decode("utf-8"))
            request = data["message"]
            address = data["address"]
            if request[0] == STOP: 
                break 
            if request[0] == LOOKUP_REQ:                       # A lookup request #-
                nextID = self.localSuccNode(request[1])          # look up next node #-
                data = {"message": (LOOKUP_REQ,request[1]), "address": str(self.node_address[nextID])} # send to succ #-
                if not self.chan.exists(nextID):
                    self.delNode(nextID) 

node= ChordNode(Address("localhost","5555"),Address("localhost","5000"))
node.run()