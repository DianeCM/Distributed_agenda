import hashlib
from termcolor import colored
import json
import socket
import zipfile

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
	
def send_request(address,data,answer_requiered,expected_zip_file):     
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
                
                if not expected_zip_file:
                  data = sender.recv(1024)
                  data = data.decode('utf-8')
                  data = json.loads(data) 
                  sender.close()
                else:
                    data= False
                    f = open("copia.db",'wb') #open in binary     
                        # receive data and write it to file
                    l = sender.recv(1024)
                    
                    while (l):
                          data = True
                          f.write(l)
                          l = sender.recv(1024)
                    f.close()
              except socket.timeout:
                # Manejar la excepción si se agotó el tiempo de espera
                if not expected_zip_file or not data: notify_data("Tiempo de espera agotado para recibir un mensaje","Error")
            sender.close()
            return data 

def notify_data(data,data_type):
	colors = {"Error":"red", "GetData": "yellow", "Join": "blue", "SetData": "magenta",'database':"green", "Check":"cyan" }
	print(colored(data,colors[data_type]))
        
def convert_into_int(bytes_seq):
    # decodifica los bytes en un entero con orden de byte 'big'
    return int.from_bytes(bytes_seq, byteorder='big')

def create_zip(zip_name,files_names):
    # Crea un archivo ZIP llamado "datos.zip"
    with zipfile.ZipFile(zip_name , "w") as mi_zip:
    # Agrega subarchivos al archivo ZIP
        for file in files_names:
          mi_zip.write(file)

def create_json_file(data,file_name):
    json_data = json.dumps(data)

    # Escribe la cadena JSON en un archivo llamado "datos.json"
    with open(file_name, "w") as f:
      f.write(json_data)
