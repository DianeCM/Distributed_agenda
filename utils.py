import hashlib

def hash_key(key: str) -> int:
    """
    Función de hash que calcula el hash SHA-1 de una cadena de caracteres y devuelve un número entero que se utiliza como la clave del nodo en la red Chord.
    """
    sha1 = hashlib.sha1(key.encode('utf-8'))
    hash_value = int(sha1.hexdigest(), 16) # convierte el hash SHA-1 en un número entero
    return hash_value

class Address(object):
		def __init__(self,ip,port):
			self.ip=ip
			self.port=port
		def __str__(self):
			return f"tcp://{self.ip}:{self.port}"

a = [166033767942643539551423125834074880812285257587, 307204989588099566025798156460738063903920132387,
      560980353103555441997218768131203573166004206993, 1380750647533812735006975667600818274455412215019]

key = 452750966148776211440986076613858788034908009627

for i in range(len(a)-1):
	if a[i] <= key < a[i+1]:
		print(a[i+1])