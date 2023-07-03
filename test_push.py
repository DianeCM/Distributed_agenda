import zmq
import json 
from constChord import *
from utils import Address
import time 

chan_address = Address("localhost","5555")
address =  Address("localhost","8888") 
def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://127.0.0.1:5557")

    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:5558")

    # Start your result manager and workers before you start your producers
    for num in range(20):
        work_message = { 'num' : num }
        zmq_socket.send_json(work_message)
        time.sleep(10)
        work = consumer_receiver.recv_json()
        data = work['num']
        print(f'recieved data {data}')
    

producer()