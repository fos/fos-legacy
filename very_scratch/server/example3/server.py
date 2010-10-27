import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 9997))
sock.listen(5)

handshake = '\
HTTP/1.1 101 Web Socket Protocol Handshake\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
WebSocket-Origin: null\r\n\
WebSocket-Location: ws://localhost:9999/\r\n\r\n\
'

handshake = '''
HTTP/1.1 101 Web Socket Protocol Handshake\r
Upgrade: WebSocket\r
Connection: Upgrade\r
WebSocket-Origin: null\r
WebSocket-Location: ws://localhost:9998/\r
WebSocket-Protocol: sample
  '''.strip() + '\r\n\r\n'
  
# WebSocket-Origin: http://localhost:8888\r\n\
handshaken = False

print "TCPServer Waiting for client on port 9998"

import sys

data = ''
header = ''
print 'hey'
client, address = sock.accept()
print 'client', client
print 'address', address


while True:
    if handshaken == False:
        header += client.recv(16)
        print 'header', header
        if header.find('\r\n\r\n') != -1:
            data = header.split('\r\n\r\n', 1)[1]
            print 'header', data
            handshaken = True
            client.send(handshake)
            print 'handshake sent'
    else:
            
            tmp = client.recv(128)
            data += tmp;

            validated = []

            msgs = data.split('\xff')
            data = msgs.pop()
            print 'data', data
            for msg in msgs:
                if msg[0] == '\x00':
                    print 'correct'
                    validated.append(msg[1:])

            for v in validated:
                print v
                client.send('\x00' + v + '\xff')