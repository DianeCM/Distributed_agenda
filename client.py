#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

class Client:
    def __init__(self):
        context = zmq.Context()
        #  Socket to talk to server
        print("Connecting to hello world server…")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")

    def run(self):
        
        #  Do 10 requests, waiting each time for a response
        for request in range(10):
            print("Sending request %s …" % request)
            self.socket.send(b"Hello")

            #  Get the reply.
            message = self.socket.recv()
            print("Received reply %s [ %s ]" % (request, message))

Client= Client()
Client.run()