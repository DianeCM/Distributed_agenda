import zmq
import random, math #-
from constChord import * #-
from utils import *
import json 
import threading
import time
import socket
from termcolor import colored

class ChordNode:

    def __init__(self,address:Address,local = False,port2 = None):

        self.address=address
        self.leader = None
        self.nodeSet = []                           # Nodes discovered so far
        self.delayed_msg = []
        self.local = local 
        self.database = {}

        self.possible_addresses =[ ("127.0.0.1",port) for port in range(5000,5010) if not str(port) == self.address.ports[1]] if self.local else [ (ip,5000) for ip in range(1,255) if not ip == self.address.ip] #verificar puerto !!!!!!!!!!!!!!!!!!!!!

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


    # INTER-NODE communication process   
    def get_discover_request(self):
        while True:
            
            conn, addr = self.discover.accept()
            # conn es otro socket que representa la conexion 
            msg=conn.recv(1024)
            msg = msg.decode('utf-8')
            msg = json.loads(msg) 
            
            request = msg["message"]

            #someone wants to contact us to join to the network
            if request == JOIN_REQ:   
                data = {"message": JOIN_REP, "ip": self.address.ip , "ports": self.address.ports , "nodeID": self.nodeID, "leader": self.leader}
                newID = msg["nodeID"]
                if not newID in self.nodeSet:
                    print(f"Receiving JOIN request from {newID}")

                    #if Im the leader 
                    if self.leader == self.nodeID:
                        self.nodeSet.append(newID)
                        self.nodeSet.sort()
                        self.recomputeFingerTable()
                        self.node_address[newID] = Address(msg["ip"],msg["ports"][0],msg["ports"][1])
                        data["nodes_ID"] = self.nodeSet                
                        data["addresses"] = { node : (address.ip,address.ports[0],address.ports[1]) for node,address in self.node_address.items()}
                    json_data = json.dumps(data).encode('utf-8')
                    conn.send(json_data)

            #A leader wants to check if Im alive
            if request == CHECK_REQ:
                data = {"message": CHECK_REP,"ip": self.address.ip , "ports": self.address.ports , "nodeID": self.nodeID, "leader": self.leader}
                newID = msg["nodeID"]
        
                print(f"Receiving CHECK request from {newID}")
                if  self.leader == self.nodeID and msg["leader"] == newID  and newID > self.nodeID:
                    
                        self.leader = newID
                json_data = json.dumps(data).encode('utf-8')
                conn.send(json_data)

            # I have a new predeccesor (sucessor)
            if request == MOV_DATA_REQ or request == REP_DATA_REQ:
                get_data =  request == MOV_DATA_REQ
                action = "MOV_DATA_REQ" if get_data else "REP_DATA_REQ"
                node = msg["nodeID"]
                print(colored(f"Receiving {action} from {node}","blue"))
                json_data = self.index_data(msg,get_data)
                conn.send(json_data)
        
    def index_data(self,msg,get_data):
        start_index = msg["startID"] if get_data else self.Predecessor
        end_index = msg["nodeID"]    if get_data else self.nodeID
        response = MOV_DATA_REP if get_data else REP_DATA_REP
        condition = lambda id : start_index <= id < end_index
        if start_index > end_index: 
            condition = lambda id : ( start_index <= id if get_data else id < end_index)
        resp_data = {id:info for id,info in self.database.items() if condition(id)}
        data = {"message": response,"ip": self.address.ip , "ports": self.address.ports , "nodeID": self.nodeID, "data":resp_data}
        return json.dumps(data).encode('utf-8')

    def send_request(self,address,data):     
            sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try : sender.connect(address)
            except ConnectionRefusedError as e :
                sender.close()
                return None
                #print("Error de conexion :", e)
                
            # establecer un tiempo de espera de 10 segundos
            sender.settimeout(10)
            json_data = json.dumps(data).encode('utf-8')

            #print("Sending Message")
            sender.send(json_data)
            try:
                # Esperar la llegada de un mensaje
                data = sender.recv(1024)
                data = data.decode('utf-8')
                data = json.loads(data) 
                sender.close()
                return data
            except socket.timeout:
                # Manejar la excepción si se agotó el tiempo de espera
                print(colored("Tiempo de espera agotado para recibir un mensaje","red"))

    def get_nodes(self,address):
            data = {"message": GET_NODES, "ip": self.address.ip , "ports": self.address.ports, "nodeID": self.nodeID,"leader":self.nodeID}
            data = self.send_request(str(self.node_address[self.leader]),data)

    # JOIN process
    def join(self):

        addresses,self.nodeSet = self.discover_nodes()

        #notify data
        print("Joined to an %s chord network as node %s" % (self.nBits,self.nodeID))
        print("Discovered nodes %s" % (self.nodeSet))

        #building node_address dict
        self.node_address = self.get_addresses(addresses)
        
        #Computing Finger Table
        self.recomputeFingerTable()
        #print("Finger Table %s " % (self.FT))
        if len(self.nodeSet) > 1:
            self.update_data(True)
            self.update_data(False)

    def discover_nodes(self):
        current_leader = 0
        leader_address = None
        discovered_nodes = [self.nodeID]
        discovered_addresses = {self.nodeID:(self.address.ip,self.address.ports[0],self.address.ports[1])}

        for address in self.possible_addresses:
            #print(f'Connecting to {address}') 
            data = {"message": JOIN_REQ, "ip": self.address.ip , "ports": self.address.ports, "nodeID": self.nodeID}
            data = self.send_request(address,data)
            if data:
                if data["message"] == JOIN_REP:
                    current_id = data["nodeID"]
                    leader = data["leader"]
                    ip = data["ip"]
                    ports = data["ports"]
                    discovered_addresses[current_id] = (ip,ports[0],ports[1])
                    discovered_nodes.append(current_id)

                    print(f'Node {current_id} discovered')

                    if leader == current_id:
                        #unpacking data
                        print(f'Leader found at node {current_id}')
                        return data["addresses"],data["nodes_ID"]
                
                    elif current_id > current_leader:
                        current_leader = current_id
                        leader_address = Address(ip,ports[0],ports[1])
                                   
        if leader_address == None:
                print(f'No node found. Setting myself as leader')
                discovered_nodes.sort()
                self.leader = self.nodeID
                thread = threading.Thread(target=self.leader_labor)
                thread .start()
                return discovered_addresses,discovered_nodes
            
        #else: Q hacer cuando ninguno de los que respondio era el lider ?????????????????? 

    def update_data(self,get_data):
        
        node = self.Sucessor if get_data else self.Predecessor
        request = MOV_DATA_REQ if get_data else REP_DATA_REQ
        response = MOV_DATA_REP if get_data else REP_DATA_REP
        receiver = "sucessor" if get_data else "predecessor"
        update_method = self.initialize_data if get_data else self.replicate_data

        print(colored(f"Connecting to {receiver} : node {node}","blue"))

        address = self.node_address[node].ip,int(self.node_address[node].ports[1])
        data = {"message": request, "ip": self.address.ip , "port": self.address.ports, "nodeID": self.nodeID}
        if get_data: data["startID"] = self.Predecessor
        data = self.send_request(address,data)
        if data["message"] == response:
                update_method(data["data"])
                print("Data updated: ",self.database)
        
    def initialize_data(self,data):
        self.database = data

    def replicate_data(self,new_data):
        for id,info in new_data.items():
            self.database [id] = info 

    
    # LEADER process            
    def leader_labor(self):
        last_nodeSet = None
        time.sleep(30)
        while self.leader == self.nodeID: 
            addresses , new_nodes= self.check_network()
            
            if not last_nodeSet or not new_nodes == last_nodeSet:
                print("New nodes",addresses)
                self.node_address = self.get_addresses(addresses)
                self.nodeSet = new_nodes
                self.recomputeFingerTable()
                self.updates_nodeSet()
                last_nodeSet = new_nodes
            else: 
                 print(f"Nodes set already update")
            time.sleep(30)

    def check_network(self):
        discovered_nodes = [self.nodeID]
        discovered_addresses = {self.nodeID:(self.address.ip,self.address.ports[0],self.address.ports[1])}
        
        for address in self.possible_addresses:
            #print(f'Connecting to {address} to check if node is alive') 
            data = {"message": CHECK_REQ, "ip": self.address.ip , "ports": self.address.ports, "nodeID": self.nodeID,"leader":self.nodeID}
            data = self.send_request(address,data)
            if data:
                if data["message"] == CHECK_REP:
                    current_id = data["nodeID"]
                    leader = data["leader"]
                    ip = data["ip"]
                    ports = data["ports"]
                    discovered_addresses[current_id] = (ip,ports[0],ports[1])
                    discovered_nodes.append(current_id)

                    print(f"Check response received from {current_id}")

                    if leader == current_id and current_id > self.nodeID:
                        print(f'There is a Leader with ID {current_id}, greater than mine. Im not leader anymore')
                        self.leader = current_id
                        return data["addresses"],data["nodes_ID"]
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


    # MAIN process
    def run(self):
        #Receiving requests
        while True:
            data = self.receiver.recv_json()

            #unpacking data
            request = data["message"]
           
            if request == STOP: 
                break 
            elif request == LOOKUP_REQ:                       # A lookup request #-
               self.lookup_key(data)               
            elif request == UPDATE_REQ:
                self.update(data)
            elif request == SET_DATA_REQ:
                self.update_key(data) 
            elif request == SET_REP_DATA_REQ:
                self.set_data(data)
            elif request == GET_DATA_REQ:
                 self.get_key(data)

    def lookup_key(self,data):
                key = data["key"]
                ip = data["ip"]
                port = data["port"]
            
                print(colored(f"Receiving LOOKUP_REQ of {key} key","green"))
                #print(self.FT)
                nextID = self.localSuccNode(key)          # look up next node #-
                consumer_sender = self.context.socket(zmq.PUSH)
                if not nextID == self.nodeID :
                    print(f"Connecting to {nextID}")
                    consumer_sender.connect(str(self.node_address[nextID]))
                    data = {"message": LOOKUP_REQ, "ip": ip , "port": port, "key": key} # send to succ
                    print(colored(f"Sending LOOKUP_REQ to {nextID} node ","green"))
                    consumer_sender.send_json(data)
                else :
                    consumer_sender.connect(f"tcp://{ip}:{port}")
                    data = {"message": LOOKUP_REP, "ip": self.address.ip , "port": self.address.ports[0], "node":  nextID,"key":key}
                    consumer_sender.send_json(data)
                consumer_sender.close()

    def update(self,data):
                print("Receiving update request")   
                self.nodeSet = data["nodeSet"]    
                print("Nodes",data["addresses"])
                self.node_address = self.get_addresses(data["addresses"])
                self.recomputeFingerTable()

    def update_key(self,data):
                key = data["key"]
                value = data["value"]
                ip = data["ip"]
                port = data["port"]
            
                print(colored(f"Receiving SET_DATA_REQ of {key} key","green"))
                nextID = self.localSuccNode(key)          # look up next node #-
                consumer_sender = self.context.socket(zmq.PUSH)
                if not nextID == self.nodeID :
                    print(f"Connecting to {nextID}")
                    consumer_sender.connect(str(self.node_address[nextID]))
                    data = {"message": SET_DATA_REQ, "ip": ip , "port": port, "key": key , "value":value} # send to succ
                    print(colored(f"Sending SET_DATA_REQ {key}:{value} to {nextID} node ","green"))
                    consumer_sender.send_json(data)
                else :
                    self.set_data(data)
                    next_node = self.FT[0]
                    if not self.nodeID == next_node:
                        consumer_sender.connect(str(self.node_address[next_node]))
                        data = {"message": SET_REP_DATA_REQ, "ip": self.address.ip , "port": self.address.ports[0], "node":  nextID,"key":key,"value":value}
                        consumer_sender.send_json(data)
                
                consumer_sender.close()

    def get_key(self,data):
                ip = data["ip"]
                port = data["port"]            
                key = data["key"]
                print(colored(f"Receiving GET_DATA_REQ of {key} key","green"))
                nextID = self.localSuccNode(key)          # look up next node #-
                consumer_sender = self.context.socket(zmq.PUSH)
                if not nextID == self.nodeID :
                    print(f"Connecting to {nextID}")
                    consumer_sender.connect(str(self.node_address[nextID]))
                    data = {"message": GET_DATA_REQ, "ip": ip , "port": port, "key": key} # send to succ
                    print(colored(f"Sending GET_DATA_REQ of {key} to {nextID} node ","green"))
                    consumer_sender.send_json(data)
                else:
                    consumer_sender.connect(f"tcp://{ip}:{port}")
                    value = self.get_data(data)
                    data = {"message": GET_DATA_REP, "ip": self.address.ip , "port": self.address.ports[0], "node":  nextID,"value": value}
                    consumer_sender.send_json(data)
                    print(colored(f"Sending  GET_DATA_REP to {ip}:{port} value: {value}","green"))
                consumer_sender.close()

    def set_data(self,data):
         key = data["key"]
         value = data["value"]
         self.database[key] = value
         print(colored(f"Set {value} to {key} key","yellow"))

    def get_data(self,data):
         key = data["key"]
         try: value = self.database[key] 
         except KeyError:
            print(colored(f"Key {key} not found","red"))
            return None
         print(colored(f"Obtained {value} to {key} key","yellow"))
         return value              
    
         

#######Tests###########################

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

