import random, math
import pickle
import os
import zmq

class Channel():

	def __init__(self, nBits=5, hostIP='redis', portNo=6379):
		self.channel   = {}
		self.channel['members']=[]
		self.osmembers = {}
		self.nBits     = nBits
		self.MAXPROC   = pow(2, nBits)
		self.addresses={}
		self.context = zmq.Context()

	def join(self, subgroup,address):
		members = self.members['members']
		newpid = random.choice(list(set([str(i) for i in range(self.MAXPROC)]) - members))
		self.channel['members'].append(str(newpid))
		try:
			self.channel[subgroup].append(str(newpid)) 
		except KeyError:
			self.channel[subgroup]=[str(newpid)]
		self.addresses[newpid]=address
		return str(newpid)

	def leave(self, subgroup,pid):
		#ospid = os.getpid()
		#pid		= self.osmembers[ospid]
		assert str(pid) in self.channel['members'], ''
		#del self.osmembers[ospid]
		self.channel['members'].remove(str(pid))
		self.channel[subgroup].remove(str(pid))
		#falta eliminar la llave de addresses
		return 

	def exists(self, pid):
		return pid in self.channel['members']

	def bind(self, pid):
		ospid = os.getpid()
		self.osmembers[ospid] = str(pid)

	def subgroup(self, subgroup):
		return self.channel[subgroup]

	def sendTo(self, caller, destinationSet, message):
		#caller = self.osmembers[os.getpid()]
		assert str(caller) in self.channel['members'], ''
		socket = self.context.socket(zmq.REQ)
		for i in destinationSet: 
			socket.connect(str(addresses[i]))
			assert str(i) in self.channel['members'], ''
			socket.send(message)
			answer = self.socket.recv() # esto creo q no deberia hacerlo aqui

    
	def sendToAll(self,caller, message):
		#caller = self.osmembers[os.getpid()]
		assert str(caller) in self.channel['members'], ''
		for i in self.channel['members']: 
			socket = context.socket(zmq.REQ)
			socket.connect(str(addresses[i]))
			socket.send(message)
			answer = self.socket.recv() # esto creo q no deberia hacerlo aqui

	def recvFromAny(self ,caller ,timeout=0):
		#caller = self.osmembers[os.getpid()]
		assert str(caller) in self.channel['members'], ''
		socket = context.socket(zmq.REP)
		socket.bind(addresses[caller])
		members = self.channel['members']
		msg = socket.recv()
		return msg
		#if msg:
		#	return [msg[0].split("'")[1],pickle.loads(msg[1])]

	def recvFrom(self, senderSet, caller, timeout=0):
		#caller = self.osmembers[os.getpid()]
		assert str(caller) in self.channel['members'], ''
		for i in senderSet: 
			assert str(i) in self.channel['members'], ''
		#xchan = [[str(i),str(caller)] for i in senderSet]
		#msg = self.channel.blpop(xchan, timeout)
		#if msg:
		#	return [msg[0].split("'")[1],pickle.loads(msg[1])]
