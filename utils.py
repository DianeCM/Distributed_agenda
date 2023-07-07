import hashlib

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
	
print(686916772571941171600637909103417451352519039489 < 753618910096819749335347094697155625726989006471 < 794143421378275501213700159784909595755571930874)

726194829332617193613155289536380227396100852965
755974421095176253786361683683136291137707119920
767083671468449695347041926955029611000155291579
776303295230970185976038826886333294512334180629

