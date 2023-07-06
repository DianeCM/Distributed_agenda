import zmq
import json 
from constChord import *
from utils import Address
import time 


#while True:
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")
socket.send(b"mensaje")
respuesta = socket.recv()
if respuesta == b"confirmacion":
        print("El mensaje ha sido entregado correctamente.")
else:
        print("No se ha recibido una confirmación de entrega.")

