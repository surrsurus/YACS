# import socket library
import socket

class Server:
	'''Server object providing ability to start a server and accept connections via sockets'''
	def __init__(self, ip, prt):
		self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ipAddress = ip
		self.port = prt

	def startServer(self):
		'''Start server and start listening/accepting connections'''
		# Bind to ip/port and start listening and accepting connections
		self.soc.bind((self.ipAddress, self.port))
		self.soc.listen(1)
		(self.connection, address) = self.soc.accept()

	# def chat(self):
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

	def recieve(self):
		'''Recieve move from client'''
		return self.soc.recv(4096).decode()

	def send(self, move):
		'''Send move from server to client'''
		self.soc.send(move.encode())
	
	def stopServer(self):
		'''Stop server'''
		self.connection.close()

IP_ADDRESS = 'localhost'
PORT = 25565
test = Server(IP_ADDRESS, PORT)
test.startServer()