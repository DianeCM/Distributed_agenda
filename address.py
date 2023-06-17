class Address(object):
		def __init__(self,ip,port):
			self.ip=ip
			self.port=port
		def __str__(self):
			return f"tcp://{self.ip}:{self.port}"