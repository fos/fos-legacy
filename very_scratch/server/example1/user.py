class user:
	user_id=0
	socket=0
	handshake=0

	def __init__(self, socket, user_id):
		self.user_id = user_id
		self.socket = socket