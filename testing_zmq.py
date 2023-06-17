from server import *
from client import * 
import os
import threading

server= Server()
client = Client()
threading.Thread(target=server.run()).start()
threading.Thread(target=client.run()).start()