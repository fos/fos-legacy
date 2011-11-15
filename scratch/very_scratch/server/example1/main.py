import websocket

class server:

	conn=0
	users=[]
	socket=0
	uid=0

	def __init__(self,address,port,connections):
		# Point Of No Return!!!
		self.socket = websocket.WebSocket(address, port, connections, self)

if __name__ == "__main__":
	print 'opening server 127.0.0.1 on port 1248'
	websocketServer = server("127.0.0.1", 1248, 1000)