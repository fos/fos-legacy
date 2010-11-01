import threading
import hashlib
import socket
import time
import re

class WebSocketThread(threading.Thread):

	def __init__ ( self, channel, details, websocket ):
		self.channel = channel
		self.details = details
		self.websocket = websocket
		threading.Thread.__init__ ( self )

	def run ( self ):
		print ("Monty> Received connection ", self.details)
		self.handshake(self.channel)
		while True:
			self.interact(self.channel)

	def finduser(self, client):
		for user in self.websocket.users:
			if user.socket == client:
				return user
		return 0

	def send_data(self, client, str):
		str = b"\x00" + str.encode('utf-8') + b"\xff"
		try:
			return client.send(str)
		except (IOError, e):
			if e.errno == 32:
				user = self.finduser(client)
				print ("Monty> pipe error")

	def recv_data(self, client, count):
		data = client.recv(count)
		return data.decode('utf-8', 'ignore')

	def get_headers(self, data):
		resource = re.compile("GET (.*) HTTP").findall(data)
		host = re.compile("Host: (.*)\r\n").findall(data)
		origin = re.compile("Origin: (.*)\r\n").findall(data)
		return [resource[0],host[0],origin[0]]

	def handshake(self, client):
		shake = self.recv_data(client, 255)
		headers = self.get_headers(shake)
		our_handshake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"+"Upgrade: WebSocket\r\n"+"Connection: Upgrade\r\n"+"WebSocket-Origin: "+headers[2]+"\r\n"+"WebSocket-Location: "+" ws://"+headers[1]+headers[0]+"\r\n\r\n"
		client.send(our_handshake.encode('utf-8'))

	def interact(self, client):
		users = self.websocket.users
		this_user = self.finduser(client)
		data = self.recv_data(client, 255)
		print (data)
		if(data[1:]=="CONNECTED"):
			self.send_data(this_user.socket, "Welcome")
		if(data[1:]=="POKE"):
			self.send_data(this_user.socket, "Quit poking me!")