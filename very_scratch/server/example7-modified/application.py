from connection import *
import datetime
import traceback

class Application:

    #
    #Constructor
    #
    def __init__(self, name):
        self.Name = name
        self.CreationTime = datetime.datetime.utcnow()
                
        self.LastTime = self.CreationTime
        self.DeltaTime = 0

        self.ConnectionTimeout = None
        
        self.Clients = []
        self.CommandMap = {}
        #which connection the current command came from
        self.CommandConnectionContext = None


    def VerifyConnection(self, connection):
        log.info("Application %s attempting to verify client..." % (self.Name))
        connection.RecvCommands()
        credentials = connection.GetNextCommand()
        log.info("Credentials %s" % (credentials))
        
        return True

    #Attempt to verify client. Return True if successful, False otherwise
    def AddClient(self, connection):
        log.info("Application %s attempting to add client..." % (self.Name))
        verified = self.VerifyConnection(connection)
        if verified == True:
            log.info("Connection was verified.")
            self.Clients.append(connection)
            connection.SetTimeout(self.ConnectionTimeout)
            return True
        else:
            log.info("Connection could not be verified.")
            return False
        
    def RemoveClient(self, connection):
        try:
            clientIndex = self.Clients.index(connection)
            connectionObject = self.Clients.pop(clientIndex)
            #Set Connected to False so the connection manager
            #knows to clean up the connection
            connectionObject.Connected = False
            log.info("Application %s dropped a client" % (self.Name))
            
        except ValueError:
            log.info("Application %s tried to drop a client that it wasn't servicing" % (self.Name))
            pass

    #attempt to look up the handler for a command and return the result of running that logic
    def ProcessCommand(self, command):
        log.info('Application %s processing a client command' % (self.Name))
        parts = command.split('|')

        #log.info('  Command map for %s: %s' % (self.Name, repr(self.CommandMap)))
        if parts[0] in self.CommandMap:
            args = parts[1:]
            result = self.CommandMap[parts[0]](*args)
            log.info('%s client Command %s returned %s' % (self.Name, command, result))
            return result
        else:
            log.info('%s got an Unknown command %s' % (self.Name, command))
            return None

    def Run(self, callback=None):
        while 1:
            try:
                #main input processing for each client
                for client in self.Clients:
                    self.CommandConnectionContext = None
                    
                    if client.Connected == True:
                        self.CommandConnectionContext = client
                        receivedCommand = client.GetNextCommand()            

                        if receivedCommand != None:
                            commandResult = self.ProcessCommand(receivedCommand)

                            if commandResult != None:
                                client.SendCommand(commandResult)
                    else:
                        self.RemoveClient(client)

                #call any custom callback logic
                if not callback == None:
                    callback()
                        
            except Exception as ex:
                self.CommandConnectionContext = None
                self.RemoveClient(client)                
                log.info('Application got an exception while servicing a client')
                log.info(repr(ex))
                traceback.print_exc()

