from application import *
from connection import *

import time
import datetime
import uuid


def Instantiate(appName='unknown'):
    gameManagerApp = GameManagerApplication(appName)
    return gameManagerApp

class GameManagerApplication(Application):
    def __init__(self, name='unknown'):
        Application.__init__(self, name)

        self.Games = {}
        
        self.CommandMap["startGame"] = self.StartGame
        self.CommandMap["stopGame"] = self.StopGame
        self.CommandMap["joinGame"] = self.JoinGame

    def Run(self):
        log.info("GameManagerApplication now running.")

        Application.Run(self, self._Run)
                
        log.info("GameManagerApplication DONE running.")

    def _Run(self):
        #Update all game instances
        completedGames = []
        
        for (guid, game) in self.Games.items():
            if game.Complete:
                completedGames.append(guid)
            elif not game.Paused:
                game.Update(0)

        for guid in completedGames:
            self.StopGame(guid)

    def StartGame(self):
        game = Game(self)
        self.Games[game.GUID] = game
        return "gameGUID|" + game.GUID

    def StopGame(self, guid):
        log.info("GameManager stopping game %s" % guid)
        game = self.Games.pop(guid, None)
        if not game == None:
            game.Stop()
            del game

    def JoinGame(self, guid, playerNum='1'):
        log.info("GameManager trying to let client join game %s" % guid)
        if guid in self.Games:
            game = self.Games[guid]
            if game.AddPlayer(self.CommandConnectionContext, playerNum):
                #Let the game instance deal with the connection
                clientIndex = self.Clients.index(self.CommandConnectionContext)
                self.Clients.pop(clientIndex)
            

class Game():
    def __init__(self, application):
        self.GUID = uuid.uuid4().hex
        self.Application = application
        self.CreationTime = datetime.datetime.utcnow()
        self.Player1 = None
        self.Player2 = None

        self.Paused = False
        self.Complete = False

    def AddPlayer(self, connection, playerNum='1'):
        if playerNum == '1' and self.Player1 == None:
            log.info("Game %s added player 1" % self.GUID)
            self.Player1 = connection
            self.Player1.SendCommand("joinedGame|" + self.GUID + "|1")
        elif playerNum == '2' and self.Player2 == None:
            log.info("Game %s added player 2" % self.GUID)
            self.Player2 = connection
            self.Player2.SendCommand("joinedGame|" + self.GUID + "|2")
        else:
            return False

        return True

    def RemovePlayer(self, playerNum='1'):
        if playerNum == '1' and not self.Player1 == None:
            self.Player1.Connected = False
            self.Player1 = None
        elif playerNum == '2' and not self.Player2 == None:
            self.Player2.Connected = False
            self.Player2 = None
        
        if self.Player1 == None and self.Player2 == None:
            self.Complete = True

    def Stop(self):
        self.RemovePlayer('1')
        self.RemovePlayer('2')

    def Update(self, deltaT):
        if self.Player1 != None and not self.Player1.Connected:
            self.Complete = True
        elif self.Player2 != None and not self.Player2.Connected:
            self.Complete = True

        
        
