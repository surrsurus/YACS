# import socket library
import socket

class Client:
	'''Client object providing ability to connect and communicate with server via sockets'''
	def __init__(self, ip, prt):
		self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ipAddress = ip
		self.port = prt

	def connect(self):
		'''Attempt connection to server (host) via IP and port'''
		print('[---------------Attempting Connection---------------]')
		try:
			self.soc.connect((self.ipAddress, self.port))
		except:
			print('[--------------Connection Unsuccessful--------------]')
			return
		print('[---------------Connection Successful---------------]')
		# Upon success, proceed to communicate
		self.communicate()

	def communicate(self):
		'''Send chat messages back/forth betweeen client and server'''
		# Client talks first. Chat continues until one party says the keyword 'goodbye'
		sentMessage = input('Enter a message or type \'goodbye\' to end the chat: ')
		while True:
			self.soc.send(sentMessage.encode())
			if sentMessage == 'goodbye':
				break
			receivedMessage = self.soc.recv(4096).decode()
			print('Server: {}'.format(receivedMessage))
			if receivedMessage == 'goodbye':
				break
			sentMessage = input('Enter a message or type \'goodbye\' to end the chat: ')
		# Upon chat termination, proceed to disconnect
		self.disconnect()
	
	def recieve(self):
		return self.soc.recv(4096).decode()

	def send(self, message):
		self.soc.send(message.encode())

	def disconnect(self):
		'''Disconnect from server'''
		self.soc.close()
		print('[--------------------Disconnected-------------------]')

IP_ADDRESS = 'localhost'
PORT = 25565
test = Client(IP_ADDRESS, PORT)
test.connect()