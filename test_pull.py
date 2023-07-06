import zmq
import threading
def run():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")
    mensaje = socket.recv()
    # procesar el mensaje
    print(mensaje)
    socket.send(b"confirmacion")

run()

thread = threading.Thread(target = run)

thread1 = threading.Thread(target= run)

thread2 = threading.Thread(target=run)

#thread.start()
#thread1.start()
#thread2.start()
