# import socket library
import socket
import pickle

class Server:
	'''Server object providing ability to start a server and accept connections via sockets'''
	def __init__(self, ip, prt):
		self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ipAddress = ip
		self.port = prt

	def startServer(self):
		'''Start server and start listening/accepting connections'''
		print('[----------------Awaiting Connection----------------]')
		# Bind to ip/port and start listening and accepting connections
		self.soc.bind((self.ipAddress, self.port))
		self.soc.listen(1)
		(self.connection, address) = self.soc.accept()
		print('[---------------Connection Successful---------------]')

	# def communicate(self):
	# 	'''Send chat messages back/forth betweeen client and server'''
	# 	# Client talks first. Chat continues until one party says the keyword 'goodbye'
	# 	while True:
	# 		receivedMessage = self.connection.recv(4096).decode()
	# 		print('Client: {}'.format(receivedMessage))
	# 		if receivedMessage == 'goodbye':
	# 			break

	# 		sentMessage = input('Enter a message or type \'goodbye\' to end the chat: ')
	# 		self.connection.send(sentMessage.encode())
	# 		if sentMessage == 'goodbye':
	# 			break

	def send(self, thing):
		self.connection.send(pickle.dumps(thing))

	def recieve(self):
		return pickle.loads(self.connection.recv(4096))

	def stopServer(self):
		'''Stop server'''
		self.connection.close()
		print('[--------------------Disconnected-------------------]')
