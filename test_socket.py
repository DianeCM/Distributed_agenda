import socket

# Crear un socket de servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket a una dirección y puerto
server_socket.bind(('localhost', 8000))

# Escuchar conexiones entrantes
server_socket.listen()

# Aceptar una conexión entrante
client_socket, address = server_socket.accept()

# Recibir datos del cliente
data = client_socket.recv(1024)

print(data)

# Cerrar el socket del cliente
client_socket.close()

# Cerrar el socket del servidor
server_socket.close()