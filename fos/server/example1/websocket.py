import socket
import wsthread
import user
import random

class WebSocket():

	uid=0
	users=[]
	server=0

	def __init__(self, address, port, connections, server):
		self.server = server
		server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
		server.bind ( ( address, port ) )
		server.listen ( connections )
		while True:
			channel, details = server.accept()
			self.uid = self.uid + 1
			self.users.append(user.user(channel, self.uid))
			wsthread.WebSocketThread (channel, details, self).start()