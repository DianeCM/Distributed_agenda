import random, math #-
from constChord import * #-
from utils import *
import json 
import threading
import time
import socket
from termcolor import colored
from peewee import *
import shutil
import zipfile
import sqlite3
import struct
from database import *
import io
import os

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
        self.db = DBModel(self.nodeID)
        self.nBits = 160
       
        #Initializing Finger Table
        self.FT = [None for i in range(self.nBits+1)]

        self.MAXPROC = pow(2,160)
        self.node_address = {}

        #initializing sockets
        
        #Cuando otro nodo de la red quiera saber si este nodo esta, debe conectarse a este socket o 
        # si este nodo es el lider el resto se conecta a este socket para actualizar su lista de nodos
        
        self.discover = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.discover.bind((self.address.ip, int(self.address.ports[1])))
        self.discover.listen()

        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.bind((self.address.ip, int(self.address.ports[0])))
        self.receiver.listen()

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
    
    @property 
    def Req_Method(self):
        return { CREATE_PROFILE: self.create_account , CREATE_GROUP: self.create_group, REP_GROUP:self.create_group, CREATE_EVENT: self.create_event, REP_PROFILE: self.create_account,
                GET_PROFILE: self.get_account,GET_GROUPS: self.get_groups_belong_to, GET_EVENTS:self.get_all_events,REP_EVENT: self.create_event, GET_NOTIFICATIONS: self.get_notifications,
                DELETE_NOTIFICATION:self.delete_notification,DELETE_NOTIFICATION_REP:self.delete_notification, ACEPT_EVENT: self.acept_pendient_event,ACEPT_EVENT_REP:self.acept_pendient_event, DELETE_EVENT: self.delete_event}
    
    @property
    def Serialize_Address(self):
        return { node : (address.ip,address.ports[0],address.ports[1]) for node,address in self.node_address.items()}

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
            msg=conn.recv(1000000)
            msg = msg.decode('utf-8')
            msg = json.loads(msg) 
            
            request = msg["message"]

            #someone wants to contact me to join to the network
            if request == JOIN_REQ:   
                data = {"message": JOIN_REP, "ip": self.address.ip , "ports": self.address.ports , "nodeID": self.nodeID, "leader": self.leader}
                newID = msg["nodeID"]
                if not newID in self.nodeSet:
                    notify_data(f"Receiving JOIN request from {newID}","Join")

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

            #Someone wants to check if Im alive
            if request == CHECK_REQ:
                data = {"message": CHECK_REP,"ip": self.address.ip , "ports": self.address.ports , "nodeID": self.nodeID, "leader": self.leader, "nodes_ID":self.nodeSet, "addresses":self.Serialize_Address }
                newID = msg["nodeID"]
                
                notify_data(f"Receiving CHECK request from {newID}","Check")
                if  self.leader == self.nodeID and msg["leader"] == newID  and newID > self.nodeID:                    
                        self.leader = newID
                json_data = json.dumps(data).encode('utf-8')
                conn.send(json_data)

            # I have a new predeccesor (sucessor)
            if request == MOV_DATA_REQ or request == REP_DATA_REQ:
                get_data =  request == MOV_DATA_REQ
                action = "MOV_DATA_REQ" if get_data else "REP_DATA_REQ"
                response =   "MOV_DATA_REP" if get_data else "REP_DATA_REP"
                node = msg["nodeID"]
                notify_data(f"Receiving {action} from {node}","GetData")
                data = self.index_data(msg,get_data)
                f = open ("copia.db", "rb")
                l = f.read(1024)
                while (l):
                    conn.send(l)
                    l = f.read(1024)
                os.remove("copia.db")
                notify_data(f"Sending {response} to {node}","GetData")
                

            if request == GET_NODES:
                id = msg["nodeID"]
                notify_data(f'Recieving GET_NODES request from {id}',"GetData")
                addresses = { node : (address.ip,address.ports[0],address.ports[1]) for node,address in self.node_address.items()}
                data = {"message": SET_NODES,"ip": self.address.ip , "ports": self.address.ports , "nodeID": self.nodeID, "nodeSet":self.nodeSet, "addresses":addresses}
                data = json.dumps(data).encode('utf-8')
                conn.send(data)

            if request == SET_LEADER:
                id = msg["nodeID"]
                notify_data(f'Recieving SET_LEADER request from {id}',"Check")
                addresses,self.nodeSet = self.discover_nodes(True)
                self.node_address = self.get_addresses(addresses) 
                self.recomputeFingerTable()
                
    def index_data(self,msg,get_data):
        start_index = msg["startID"] if get_data else self.Predecessor
        end_index =   msg["nodeID"]  if get_data else self.nodeID
        print(start_index,end_index)
        condition = lambda id : self.inbetween(int(id),start_index,end_index)
        self.db.get_filtered_db(condition,'copia.db')


    def get_nodes(self):           
            data = {"message": GET_NODES, "ip": self.address.ip , "ports": self.address.ports, "nodeID": self.nodeID}
            leader_address = self.node_address[self.leader] 
            data = send_request((leader_address.ip,int(leader_address.ports[1])),data,True,False)
            if data:
              if data["message"] == SET_NODES:
                self.nodeSet = data["nodeSet"]
                notify_data(f"Upadating node set :{self.nodeSet}","GetData")
                self.node_address = self.get_addresses(data["addresses"])
                self.recomputeFingerTable()
              else:
                msg = data["message"]
                notify_data(f"Not expected {msg} !!!!!!!!!!!!!!!!","Error")
            else:
                addresses,self.nodeSet = self.discover_nodes(True)
                #building node_address dict
                self.node_address = self.get_addresses(addresses)       
                #Computing Finger Table
                self.recomputeFingerTable()
                 
    # JOIN process
    def join(self):

        addresses,self.nodeSet = self.discover_nodes(False)

        #notify data
        notify_data("Joined to an %s chord network as node %s" % (self.nBits,self.nodeID),"Join")
        notify_data("Discovered nodes %s" % (self.nodeSet),"Join")

        #building node_address dict
        self.node_address = self.get_addresses(addresses)
        
        #Computing Finger Table
        self.recomputeFingerTable()
        #print("Finger Table %s " % (self.FT))
        if len(self.nodeSet) > 1:
            self.update_data(True)
            self.update_data(False)

    def discover_nodes(self,find_leader):
        current_leader = self.nodeID
        leader_address = self.address
        discovered_nodes = [self.nodeID]
        discovered_addresses = {self.nodeID:(self.address.ip,self.address.ports[0],self.address.ports[1])}
        msg_to_send = CHECK_REQ if find_leader else JOIN_REQ
        msg_to_rcv  = CHECK_REP if find_leader else JOIN_REP
        for address in self.possible_addresses:
            #print(f'Connecting to {address}') 
            data = {"message": msg_to_send, "ip": self.address.ip , "ports": self.address.ports, "nodeID": self.nodeID, "leader":self.leader,"nodeSet":self.nodeSet}
            data = send_request(address,data,True,False)
            if data:
                if data["message"] == msg_to_rcv:
                    current_id = data["nodeID"]
                    leader = data["leader"]
                    ip = data["ip"]
                    ports = data["ports"]
                    discovered_addresses[current_id] = (ip,ports[0],ports[1])
                    discovered_nodes.append(current_id)

                    notify_data(f'Node {current_id} discovered',"Join")

                    if leader == current_id:
                        self.leader = current_id
                        notify_data(f'Leader found at node {current_id}',"Join")
                        return data["addresses"],data["nodes_ID"]
                
                    elif current_id > current_leader:
                        current_leader = current_id
                        leader_address = Address(ip,ports[0],ports[1])
                                   
        if current_leader == self.nodeID:
                notify_data('Setting myself as leader',"Join")
                discovered_nodes.sort()
                self.leader = self.nodeID
                thread = threading.Thread(target=self.leader_labor)
                thread .start()
        else: 
            notify_data(f'Greatest node found : {current_leader}. That one is the leader',"Join")
            data = {"message": SET_LEADER, "ip": self.address.ip, "ports": self.address.ports, "nodeID": self.nodeID, "leader":self.leader,"nodeSet":self.nodeSet}
            send_request((leader_address.ip,int(leader_address.ports[1])),data,False,False)
            discovered_nodes.sort()
            self.leader = current_leader

        return discovered_addresses,discovered_nodes   
    
    def update_data(self,get_data):
        
        node = self.Sucessor if get_data else self.Predecessor
        request = MOV_DATA_REQ if get_data else REP_DATA_REQ
        response = MOV_DATA_REP if get_data else REP_DATA_REP
        receiver = "sucessor" if get_data else "predecessor"
        update_method = self.initialize_data if get_data else self.db.replicate_db
        
        notify_data(f"Connecting to {receiver} : node {node}","GetData")

        address = (self.node_address[node].ip,int(self.node_address[node].ports[1]))
        data = {"message": request, "ip": self.address.ip , "port": self.address.ports, "nodeID": self.nodeID}
        if get_data: data["startID"] = self.Predecessor
        successfull = send_request(address,data,True,True)
        #falta comprobar que llego el mensaje completo !!!!!!!!!!!!!!!!!!
        if successfull:
            update_method('copia.db')
            notify_data(f"Data updated","database")
            self.db.check_db()
            os.remove('copia.db')


    def initialize_data(self,db_name):
        shutil.copyfile(db_name,self.db.db_name)
 
    # LEADER process            
    def leader_labor(self):
        time.sleep(30)
        while self.leader == self.nodeID: 
            addresses , new_nodes = self.check_network()

            if  not (new_nodes == self.nodeSet):
                self.node_address = self.get_addresses(addresses)
                self.nodeSet = new_nodes
                notify_data(f"New nodes {self.node_address}","Join")
                self.recomputeFingerTable()
            else: 
                notify_data(f"Nodes set already update","Check")
                notify_data(f"Nodes {self.node_address}","Join")
                #self.recomputeFingerTable()
                #print(self.FT)
            time.sleep(30)

    def check_network(self):
        discovered_nodes = [self.nodeID]
        discovered_addresses = {self.nodeID:(self.address.ip,self.address.ports[0],self.address.ports[1])}
        
        for address in self.possible_addresses:
            #print(f'Connecting to {address} to check if node is alive') 
            data = {"message": CHECK_REQ, "ip": self.address.ip , "ports": self.address.ports, "nodeID": self.nodeID,"leader":self.nodeID}
            data = send_request(address,data,True,False)
            if data:
                if data["message"] == CHECK_REP:
                    current_id = data["nodeID"]
                    leader = data["leader"]
                    ip = data["ip"]
                    ports = data["ports"]
                    discovered_addresses[current_id] = (ip,ports[0],ports[1])
                    discovered_nodes.append(current_id)

                    notify_data(f"Check response received from {current_id}","Check")

                    if leader == current_id and current_id > self.nodeID:
                        notify_data(f'There is a Leader with ID {current_id}, greater than mine. Im not leader anymore',"Join")
                        self.leader = current_id
                        return data["addresses"],data["nodes_ID"]
        discovered_nodes.sort()
        return discovered_addresses, discovered_nodes


    # MAIN process
    def run(self):
        #Receiving requests
        while True:
            print("next_step")
            
            print(f"My address: {str(self.address)}")
            conn, addr = self.receiver.accept()
            msg=conn.recv(1000000)
            msg = msg.decode('utf-8')
            data = json.loads(msg) 

            #unpacking data
            request = data["message"]
           
            if request == STOP: 
                break
            elif request in self.Req_Method.keys():
                notify_data(f"Receiving {request} from {addr}","SetData")
                if 30 <= int(request) < 60:
                    if not self.leader == self.nodeID: self.get_nodes()   
                    if int(request)%2 ==0 :self.update_key(data,request,addr)
                    else: 
                        self.Req_Method[request](data)
                        self.db.check_db()
                if 60 <= int(request) < 80:
                   if not self.leader == self.nodeID: self.get_nodes()
                   self.get_key(data,request)

            #elif request == LOOKUP_REQ: 
            #   if not self.leader == self.nodeID: self.get_nodes()                  # A lookup request #-
            #   self.lookup_key(data)               

            #elif request == SET_DATA_REQ:
            #    p = data["port"]
            #    print(self.address.ports[0])
            #    notify_data(f"Receiving SET_DATA_REQ from {p}","GetData")
            #    if not self.leader == self.nodeID: self.get_nodes()                
            #    self.update_key(data) 

            #elif request == GET_DATA_REQ:
            #    notify_data(f"Receiving GET_DATA_REQ","GetData")
            #    if not self.leader == self.nodeID: self.get_nodes()
            #    self.get_key(data,addr)
            
    def lookup_key(self,data):
                key = data["key"]
                ip = data["ip"]
                port = data["port"]
            
                notify_data(f"Receiving LOOKUP_REQ of {key} key","GetData")
                #print(self.FT)
                nextID = self.localSuccNode(key)          # look up next node #-
                
                if not nextID == self.nodeID :
                    #notify_data(f"Connecting to {nextID}","GetData")
                    data = {"message": LOOKUP_REQ, "ip": ip , "port": port, "key": key} # send to succ
                    send_request((self.node_address[nextID].ip,int(self.node_address[nextID].ports[0])),data,False,False)
                    notify_data(f"Sending LOOKUP_REQ to {nextID} node ","Get_Data")
                else:
                    data = {"message": LOOKUP_REP, "ip": self.address.ip , "port": self.address.ports[0], "node":  nextID,"key":key}        
                    send_request((ip,int(port)),data,False,False)               

    def update_key(self,data,request,addr):
                key = data["user_key"]
                nextID = self.localSuccNode(key)          # look up next node #-
                
                if not nextID == self.nodeID :
                    #data = {"message": request, "ip": ip , "port": self.address.ports[0], "user_key": key } # send to succ                    
                    notify_data(f"Sending {request}  to {nextID}: {str(self.node_address[nextID])} node ","SetData")
                    send_request((self.node_address[nextID].ip,int(self.node_address[nextID].ports[0])),data,False,False)
                else :
                    self.Req_Method[request](data)
                    self.db.check_db()
                    next_node = self.FT[1]
                    if not self.nodeID == next_node:
                        notify_data(f"Sending {int(request)+1} to {next_node}","SetData")
                        #data = {"message": str(int(request)+1), "ip": self.address.ip , "port": self.address.ports[0], "node":  nextID,"user_key":key}
                        data["message"] = str(int(request)+1)
                        send_request((self.node_address[next_node].ip,int(self.node_address[next_node].ports[0])),data,False,False)  

    def get_key(self,data,request):            
                key = data["user_key"]
                sender_addr = data["sender_addr"]
                nextID = self.localSuccNode(key)          # look up next node #-
                if not nextID == self.nodeID :
                    #data = {"message": request, "ip": ip , "port": port, "key": key,"sender_addr":sender_addr } # send to succ 
                    send_request((self.node_address[nextID].ip,int(self.node_address[nextID].ports[0])),data,False,False)
                    notify_data(f"Sending {request} to {nextID} node : {str(self.node_address[nextID])} ","GetData")
                else:
                    data = self.Req_Method[request](data)
                    #data = self.get_data(data,int(request)+1)
                    notify_data(f"Sending  {int(request)+1} to {sender_addr}","GetData")
                    send_request((sender_addr[0],sender_addr[1]),data,False,False)
                    
    def set_data(self,data):
        key = data["key"]
        value = data["value"]
        self.database[key] = value
        notify_data(f"Set {value} to {key} key","SetData")

    def get_data(self,data):
        key = data["key"]
        try: value = self.database[key] 
        except KeyError:
           notify_data(colored(f"Key {key} not found","Error"))
           return None
        notify_data(f"Obtained {value} to {key} key","GetData")
        return value              
    
    def create_account(self,data):
        self.db.create_account(data["user_key"],data["user_name"],data["last_name"],data["password"])

    def get_account(self,data):
        response = str(int(data["message"])+1)
        user_name,last_name=self.db.get_account(data["user_key"],data["password"])
        resp_data = {"message": str(response),'user_name':user_name,'last_name':last_name}
        if  user_name and last_name:
            resp_data["ip"] = data["ip"] 
            resp_data["port"] = data["port"] 
            resp_data["sender_addr"] = data["sender_addr"]
            return resp_data
        else:
            notify_data("This account doesn't exist","Error")
    
    def create_group(self,data):
        self.db.create_group(data["user_key"],data["group_name"],data["group_type"])
    
    def get_notifications(self,data):
        ids,texts=self.db.get_notifications(data["user_key"])
        resp_data = {"message": GET_NOTIF_RESP,'ids': ids,'texts': texts}
        resp_data["ip"] = data["ip"] 
        resp_data["port"] = data["port"] 
        resp_data["sender_addr"] = data["sender_addr"]
        return resp_data

    def delete_notification(self,data):
        self.db.delete_notification(data["user_key"],data["id_notification"])

    def create_event(self,data):
        self.db.create_event(data["user_key"],data["id_event"],data["event_name"],data["date_initial"],data["date_end"],data["state"],data["visibility"],data["group"],data["creator"])

    def get_all_events(self,data):
        idevents,enames,datesc,datesf,states,visibs,creators,idgroups=self.db.get_all_events(data["user_key"])
        resp_data = {"message": GET_EVENTS_RESP, "ids_event": idevents, "event_names": enames, "dates_ini": datesc, "dates_end": datesf, 
                     "states": states, "visibilities": visibs, "creators": creators, "id_groups": idgroups  }
        resp_data["ip"] = data["ip"] 
        resp_data["port"] = data["port"] 
        resp_data["sender_addr"] = data["sender_addr"]
        return resp_data
    
    def get_groups_belong_to(self,data):
        idsgroup,gnames,gtypes,refs = self.db.get_groups_belong_to(data["user_key"])
        resp_data = {"message": GET_GROUPS_RESP, "ids_group": idsgroup, "group_names": gnames, "group_types": gtypes, "group_refs": refs  }
        resp_data["ip"] = data["ip"] 
        resp_data["port"] = data["port"] 
        resp_data["sender_addr"] = data["sender_addr"]
        return resp_data 
      
    def acept_pendient_event(self,data):
        self.db.acept_pendient_event(data["user_key"],data["id_event"])

    def delete_event(self,data):
        user_key = data["user_key"] 
        id_event = data["id_evet"]
        self.db.delete_event(user_key,id_event) 