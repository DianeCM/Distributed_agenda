import hashlib
from termcolor import colored
import json
import socket

def hash_key(key: str) -> int:
    """
    Función de hash que calcula el hash SHA-1 de una cadena de caracteres y devuelve un número entero que se utiliza como la clave del nodo en la red Chord.
    """
    sha1 = hashlib.sha1(key.encode('utf-8'))
    hash_value = int(sha1.hexdigest(), 16) # convierte el hash SHA-1 en un número entero
    return hash_value

class Address(object):
		def __init__(self,ip,port1,port2):
			self.ip=ip
			self.ports = (port1,port2)
			
		def __str__(self):
			return f"tcp://{self.ip}:{self.ports[0]}"
	
def send_request(address,data,answer_requiered):     
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
            if answer_requiered:
              try:
                # Esperar la llegada de un mensaje
                data = sender.recv(1024)
                data = data.decode('utf-8')
                print(data)
                data = json.loads(data) 
                sender.close()
                return data
              except socket.timeout:
                # Manejar la excepción si se agotó el tiempo de espera
                notify_data("Tiempo de espera agotado para recibir un mensaje","Error")
            sender.close()



def notify_data(data,data_type):
	colors = {"Error":"red", "GetData": "yellow", "Join": "blue", "SetData": "magenta",'database':"green", "Check":"cyan" }
	print(colored(data,colors[data_type]))
