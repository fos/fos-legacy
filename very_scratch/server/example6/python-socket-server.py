import socket
import select
import time
import handler
import tick
import settings

cycles_per_tick = settings.cycles_per_tick
port = settings.port
hostname = settings.hostname
websocket_location = settings.websocket_location
#'192.168.56.1'
#'68.98.117.248' 
#socket.gethostname() 
#"127.0.0.1" 
#"192.168.1.104"




hostname = hostname.lower() #important
scope = {}
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((hostname, port)) #this is the one you want
hnp = hostname + ":" + str(port)
print "go to http://" + hnp
serversocket.listen(5)
serversocket.setblocking(0)
#serversocket.settimeout(10000);
#serversocket.settimeout(.01);
def handle_data(data, socko, to_read, to_write, to_error):
    if data[0:len("<policy-file-request/>")] == "<policy-file-request/>":
        socko.send( '<?xml version=\"1.0\"?><cross-domain-policy><allow-access-from domain="*" to-ports= "*" /></cross-domain-policy>')
        print "sent policy file"
        closesocket(socko)
    elif data[0:55] == "GET / HTTP/1.1\r\nUpgrade: WebSocket\r\nConnection: Upgrade":
        websocket_response = u"HTTP/1.1 101 Web Socket Protocol Handshake\r\nUpgrade: WebSocket\r\nConnection: Upgrade\r\nWebSocket-Origin: http://"+ hnp +"\r\nWebSocket-Location: ws://"+ hnp + websocket_location + "\r\n\r\n"
        socko.send(websocket_response)
        print websocket_response
        print "web socky"
    elif data[0:14] == "GET / HTTP/1.1": #normal http
        file = open("index.html", "r")
        contents = file.read()
        contents =  contents.replace("ws://host_here:port_here/", "ws://" + hnp + websocket_location )
        print "normal http"
        socko.send("HTTP/1.1 200 OK\r\n" 
        "Connection: close\r\n" +
        "Content-Type: text/html\r\n" +
        "Content-Length: " + str(len(contents)) + "\r\n\r\n" +
        contents)
    elif data[0:25] == "GET /favicon.ico HTTP/1.1":
        print "favicon"
        contents = open("favicon.png", "rb").read()
        socko.send("HTTP/1.1 200 OK\r\n" 
        "Connection: close\r\n" +
        "Content-Type: image/png\r\n" +
        "Content-Length: " + str(len(contents)) + "\r\n\r\n" +
        contents)
    elif (data[0] == "\x00" and data[-1] == "\xff"): #websocket format
        handler.handle(data[1:-1], socko, to_read, to_write, to_error, scope)
    else:
        print "you said"
        print data
        for i in data:
            print ord(i)
connections = [serversocket]
conn_info = [];
counter = 0;
def closesocket(socko):
    socko.close()
    connections.remove(socko) #remove is pretty cool if it works!
    socko = None
while True:
    counter = counter + 1
    time.sleep(.001) #change this in the future for speed
    to_read, to_write, to_error = select.select(connections,connections,connections,0)
    for socko in to_read:
        if socko == serversocket:
            print "connecting"		
            (clientsocket, address) = socko.accept()
            print "putting " + address[0] + " onto connections";
            conn_info.append(address)
            clientsocket.setblocking(0)
            connections.append(clientsocket)
            print len(connections)
        else:
            print "reader"
            try:  #i needed this try block only for google chrome! wierd.
                data = socko.recv(1024) #1024 potential problem causer
            except socket.error, msg:
                closesocket(socko)
                break
            print data
            if not data:
                print "no data"
                closesocket(socko)
                break
            try:
                handle_data(data, socko, to_read, to_write, to_error)
            except socket.error, msg:
                closesocket(socko)
    if counter % cycles_per_tick == 0:
        print connections
        tick.tick(to_read, to_write, to_error, scope)
    for socko in to_error:
        print socko + " had an error"            