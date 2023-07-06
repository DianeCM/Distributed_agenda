import zmq
import channel #-
import random, math #-
from constChord import * #-
from utils import *
import json 
import threading
import time
import socket

class ChordNode:

    def __init__(self,address:Address,local = False,port2 = None):

        self.address=address
        self.leader = None
        self.nodeSet = []                           # Nodes discovered so far
        self.delayed_msg = []
        self.local = local 

        #Setting node ID
        key = address.ip if not local else str(self.address)
        self.nodeID = hash_key(key) ## Cambiar por el ID

        self.nBits = 160
       
        #Initializing Finger Table
        self.FT = [None for i in range(self.nBits+1)]

        self.MAXPROC = pow(2,160)
        self.node_address = {}

        #initializing sockets

        self.context = zmq.Context()

        #socket al cual seran enviados todos los request que no sean de descubrimiento 

        self.receiver = self.context.socket(zmq.PULL)       
        self.receiver.bind(str(self.address))

        #Cuando otro nodo de la red quiera saber si este nodo esta, debe conectarse a este socket o 
        # si este nodo es el lider el resto se conecta a este socket para actualizar su lista de nodos
        
        self.discover = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.discover.bind((self.address.ip, int(self.address.ports[1])))
        self.discover.listen()

        self.join()

        self.discover_resp_thread = threading.Thread(target=self.get_discover_request)
        self.discover_resp_thread .start()

        self.run()
        
    @property
    def Predecessor(self):
        return self.FT[0]
    
    @property 
    def Sucessor(self):
        return self.FT[1]
    
    def inbetween(self, key, lwb, upb):                                         
        if lwb <= upb:                                                            
            return lwb <= key < upb                                                                                                         
        return (lwb <= key and key < upb + self.MAXPROC) or (lwb <= key + self.MAXPROC and key < upb)                        

    def finger(self, i):
        succ = (self.nodeID + pow(2, i-1)) % self.MAXPROC    # succ(p+2^(i-1))
        lwbi = self.nodeSet.index(self.nodeID)               # own index in nodeset
        upbi = (lwbi + 1) % len(self.nodeSet)                # index next neighbor
        for _ in range(len(self.nodeSet)):                   # go through all segments
            if self.inbetween(succ, self.nodeSet[lwbi]+1, self.nodeSet[upbi]+1):
                return self.nodeSet[upbi]                        # found successor
            (lwbi,upbi) = (upbi, (upbi+1) % len(self.nodeSet)) # go to next segment
        return None                                                                
    
    def recomputeFingerTable(self):
        if len(self.nodeSet) > 1:
            self.FT[0]  = self.nodeSet[self.nodeSet.index(self.nodeID)-1] # Predecessor
            self.FT[1:] = [self.finger(i) for i in range(1,self.nBits+1)] # Successors
        elif len(self.nodeSet)  == 1: self.FT = [self.nodeSet[0] for i in range(1,self.nBits+1)]

        #actualizar data

    def localSuccNode(self, key): 
        if self.inbetween(key, self.FT[0]+1, self.nodeID+1): # key in (FT[0],self]
            return self.nodeID                                 # node is responsible
        elif self.inbetween(key, self.nodeID+1, self.FT[1]): # key in (self,FT[1]]
            return self.FT[1]                                  # successor responsible
        for i in range(1, self.nBits+1):                     # go through rest of FT
            if self.inbetween(key, self.FT[i], self.FT[(i+1) % self.nBits]):
                return self.FT[i]                                # key in [FT[i],FT[i+1])
    
    def get_addresses(self,addresses):
        return {int(node):Address(address[0],address[1],address[2]) for node,address in addresses.items()}

    def discover_nodes(self):
        addresses  = [ ("127.0.0.1",port) for port in range(5000,5010) if not str(port) == self.address.ports[1]] if self.local else [ f"tcp://{ip}:{5000}" for ip in range(1,255) if not ip == self.address.ip] #verificar puerto !!!!!!!!!!!!!!!!!!!!!

        current_leader = 0
        leader_address = None
        discovered_nodes = [self.nodeID]
        discovered_addresses = {self.nodeID:(self.address.ip,self.address.ports[0],self.address.ports[1])}

        for address in addresses:
            print(f'Connecting to {address}') 
            
            sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try :sender.connect(address)
            except ConnectionRefusedError as e :
                print("Error de conexion :", e)    
                continue

            # establecer un tiempo de espera de 1 segundos
            sender.settimeout(10)

            data = {"message": JOIN_REQ, "ip": self.address.ip , "ports": self.address.ports, "nodeID": self.nodeID}
            json_data = json.dumps(data).encode('utf-8')

            print("Sending Message")
            sender.send(json_data)

            try:
                # Esperar la llegada de un mensaje
                data = sender.recv(1024)
                data = data.decode('utf-8')
                data = json.loads(data) 

                if data["message"] == JOIN_REP:
                    current_id = data["nodeID"]
                    leader = data["leader"]
                    ip = data["ip"]
                    ports = data["ports"]
                    discovered_addresses[current_id] = (ip,ports[0],ports[1])
                    discovered_nodes.append(current_id)

                    print(f'Node {current_id} discovered')

                    if leader == current_id:
                        sender.close()
                        #unpacking data
                        print(f'Leader found at node {current_id}')
                        return data["addresses"],data["nodes_ID"]
                
                    elif current_id > current_leader:
                        current_leader = current_id
                        leader_address = Address(ip,ports[0],ports[1])
                        
            except socket.timeout:
                # Manejar la excepción si se agotó el tiempo de espera
                print("Tiempo de espera agotado para recibir un mensaje")

           
            sender.close()
                
            
        if leader_address == None:
                print(f'No node found. Setting myself as leader')
                discovered_nodes.sort()
                self.leader = self.nodeID
                thread = threading.Thread(target=self.leader_labor)
                thread .start()

                return discovered_addresses,discovered_nodes
            
            #else: Q hacer cuando ninguno de los que respondio era el lider ?????????????????? 
       
    def get_nodes(self):
        consumer_sender = self.context.socket(zmq.PUSH)
        consumer_sender.connect(str(self.node_address[self.leader]))
        data = {"message": GET_NODES, "ip": self.address.ip , "port": self.address.port, "nodeID": self.nodeID}
        consumer_sender.send_json(data)

    def get_discover_request(self):
        while True:
            
            conn, addr = self.discover.accept()
            # conn es otro socket que representa la conexion 
            msg=conn.recv(1024)
            msg = msg.decode('utf-8')
            msg = json.loads(msg) 
            
            #someone wants to contact us to join to the network
            if msg["message"] == JOIN_REQ:   
                data = {"message": JOIN_REP, "ip": self.address.ip , "ports": self.address.ports , "nodeID": self.nodeID, "leader": self.leader}
                newID = msg["nodeID"]
                if not newID in self.nodeSet:
                    print(f"Receiving JOIN request from {newID}")

                    #if Im the leader 
                    if self.leader == self.nodeID:
                        self.nodeSet.append(newID)
                        self.nodeSet.sort()
                        self.node_address[newID] = Address(msg["ip"],msg["ports"][0],msg["ports"][1])
                        data["nodes_ID"] = self.nodeSet                
                        data["addresses"] = { node : (address.ip,address.ports[0],address.ports[1]) for node,address in self.node_address.items()}
                    json_data = json.dumps(data).encode('utf-8')
                    conn.send(json_data)

            #A leader wants to check if Im alive
            if msg["message"] == CHECK_REQ:
                data = {"message": CHECK_REP,"ip": self.address.ip , "ports": self.address.ports , "nodeID": self.nodeID, "leader": self.leader}
                newID = msg["nodeID"]
        
                print(f"Receiving CHECK request from {newID}")
                if  self.leader == self.nodeID and newID < self.nodeID:
                        self.nodeSet.append(newID)
                        self.nodeSet.sort()
                        self.node_address[newID] = Address(msg["ip"],msg["ports"][0],msg["ports"][1])
                        data["nodes_ID"] = self.nodeSet                
                        data["addresses"] = { node : (address.ip,address.ports[0],address.ports[1]) for node,address in self.node_address.items()}
                        self.leader = newID
                json_data = json.dumps(data).encode('utf-8')
                conn.send(json_data)

    def join(self):

        addresses,self.nodeSet = self.discover_nodes()

        #notify data
        print("Joined to an %s chord network as node %s" % (self.nBits,self.nodeID))
        print("Discovered nodes %s" % (self.nodeSet))

        #building node_address dict
        self.node_address = self.get_addresses(addresses)
        
        #Computing Finger Table
        self.recomputeFingerTable()
        print("Finger Table %s " % (self.FT))

        #self.update_data()

    def update_data(self):
        
        print("Conecting to sucessor")
        consumer_sender = self.context.socket(zmq.PUSH)
        consumer_sender.connect(str(self.node_address[self.Sucessor]))

        #Send a message to sucessor to get own data
        print("Sending a message to sucessor to get own data")
        data = {"message": SET_PRED, "ip": self.address.ip , "port": self.address.port, "nodeID": self.nodeID}
        consumer_sender.send_json(data)
        consumer_sender.close()

        #como enviar toda la informacion correspondiente a un usuario, de un nodo a otro?????????????????????????

        data = self.receiver.recv_json() 

        #Recieving own data !!!!!!!!!!!!!!!

        #Updating own data !!!!!!!!!!!!!!!!!!!

        print("Conecting to predecessor")
        consumer_sender = self.context.socket(zmq.PUSH)
        consumer_sender.connect(str(self.node_address[self.Predecessor]))

        #Send a message to predecessor to replicate his data
        print("Sending a message to predecessor to replicate his data")
        data = {"message": SET_SUC, "ip": self.address.ip , "port": self.address.port, "nodeID": self.nodeID}
        consumer_sender.send_json(data)
        consumer_sender.close()

        #como enviar toda la informacion correspondiente a un usuario, de un nodo a otro?????????????????????????

        data = self.receiver.recv_json() 

        #Recieving own data !!!!!!!!!!!!!!!

        #Updating own data !!!!!!!!!!!!!!!!!!!

    def run(self):
        #Receiving requests
        while True:

            data = self.receiver.recv_json()

            #unpacking data
            request = data["message"]
            ip = data["ip"]
            port = data["port"]
            
            if request == STOP: 
                break 
            if request == LOOKUP_REQ:                       # A lookup request #-
                
                key = data["key"]
                print(f"Receiving LOOKUP_REQ of {key} key")
                print(self.FT)
                nextID = self.localSuccNode(key)          # look up next node #-
                consumer_sender = self.context.socket(zmq.PUSH)
                if not nextID == self.nodeID :
                    print(f"Connecting to {nextID}")
                    consumer_sender.connect(str(self.node_address[nextID]))
                    data = {"message": LOOKUP_REQ, "ip": ip , "port": port, "key": key} # send to succ
                    print(f"Sending LOOKUP_REQ to {nextID} node ")
                    consumer_sender.send_json(data)
                else :
                    consumer_sender.connect(f"tcp://{ip}:{port}")
                    data = {"message": LOOKUP_REP, "ip": self.address.ip , "port": self.address.ports[0], "node":  nextID,"key":key}
                    consumer_sender.send_json(data)
                consumer_sender.close()
            #if request == LOOKUP_REP:
            #    consumer_sender.connect(str(self.chan_address))
            #    node = data["node"]
            #    data = {"message": LOOKUP_REP, "ip": self.address.ip , "port": self.address.port, "node": node , "key":key}
            #    consumer_sender.send_json(data)
            #    consumer_sender.close()

            if request == UPDATE_REQ:
                print("Receiving update request")   
                self.nodeSet = data["nodeSet"]    
                print("Nodes",data["addresses"])
                self.node_address = self.get_addresses(data["addresses"])
                self.recomputeFingerTable()

    def leader_labor(self):
        time.sleep(30)
        while self.leader == self.nodeID: 
            addresses , self.nodeSet = self.check_network()
            print("New nodes",addresses)
            self.node_address = self.get_addresses(addresses)
            self.recomputeFingerTable()
            self.updates_nodeSet()
            time.sleep(30)

    def check_network(self):
        addresses  = [ ("127.0.0.1",port) for port in range(5000,5010) if not str(port) == self.address.ports[1]] if self.local else [ f"tcp://{ip}:{5000}" for ip in range(1,255) if not ip == self.address.ip] #verificar puerto !!!!!!!!!!!!!!!!!!!!!
        discovered_nodes = [self.nodeID]
        discovered_addresses = {self.nodeID:(self.address.ip,self.address.ports[0],self.address.ports[1])}
        
        for address in addresses:
            print(f'Connecting to {address} to check if node is alive') 
            
            sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try : sender.connect(address)
            except ConnectionRefusedError as e :
                print("Error de conexion :", e)
                continue

            # establecer un tiempo de espera de 1 segundos
            sender.settimeout(10)

            data = {"message": CHECK_REQ, "ip": self.address.ip , "ports": self.address.ports, "nodeID": self.nodeID}
            json_data = json.dumps(data).encode('utf-8')

            print("Sending Message")
            sender.send(json_data)
            try:
                # Esperar la llegada de un mensaje
                data = sender.recv(1024)
                data = data.decode('utf-8')
                data = json.loads(data) 
          
                if data["message"] == CHECK_REP:
                    current_id = data["nodeID"]
                    leader = data["leader"]
                    ip = data["ip"]
                    ports = data["ports"]
                    discovered_addresses[current_id] = (ip,ports[0],ports[1])
                    discovered_nodes.append(current_id)

                    print(f"Check response received from {current_id}")

                    if leader == current_id and current_id > self.nodeID:
                        sender.close()
                        #unpacking data
                        print(f'There is a Leader with ID {current_id}, greater than mine. Im not leader anymore')
                        self.leader = current_id
                        
                        return data["addresses"],data["nodes_ID"]
                        
            except socket.timeout:
                # Manejar la excepción si se agotó el tiempo de espera
                print("Tiempo de espera agotado para recibir un mensaje")
           
            sender.close()
            discovered_nodes.sort()
        return discovered_addresses, discovered_nodes

    def updates_nodeSet(self):
        addresses = { node : (address.ip,address.ports[0],address.ports[1]) for node,address in self.node_address.items()}
        for node in self.nodeSet:
            if not node == self.nodeID:
                consumer_sender = self.context.socket(zmq.PUSH)
           
                consumer_sender.connect(str(self.node_address[node]))
                data = {"message": UPDATE_REQ, "ip": self.address.ip , "port": self.address.ports[0], "nodeSet": self.nodeSet, "addresses": addresses} # send to succ
                print(f"Sending update request to node {node}",str(self.node_address[node]))
                consumer_sender.send_json(data)
        consumer_sender.close()


#node= ChordNode(Address("127.0.0.1","5050","5001"), local= True)
#thread = threading.Thread(target=node.run)

#node1= ChordNode(Address("127.0.0.1","5030","5002"), local= True)
#thread1 = threading.Thread(target=node1.run)

#node2= ChordNode(Address("127.0.0.1","5123","5006"), local= True)
#thread2 = threading.Thread(target=node2.run)

#node3= ChordNode(Address("127.0.0.1","5132","5008"), local= True)
#thread3 = threading.Thread(target=node2.run)

#thread.start()
#thread1.start()
#thread2.start()
#thread3.start()

