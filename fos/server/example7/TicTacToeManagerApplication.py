from application import *
from connection import *

import time
import datetime
import uuid


def Instantiate(appName='unknown'):
    log.info("TicTacToeManagerApplication -- Instantiate")
    app = TicTacToeManagerApplication(appName)
    return app

class TicTacToeManagerApplication(Application):
    def __init__(self, name='unknown'):
        Application.__init__(self, name)

        self.Games = {}
        
        self.CommandMap["startGame"] = self.StartGame
        self.CommandMap["stopGame"] = self.StopGame
        self.CommandMap["joinGame"] = self.JoinGame

    def Run(self):
        log.info("TicTacToeManagerApplication now running.")

        Application.Run(self, self._Run)
                
        log.info("TicTacToeManagerApplication DONE running.")

    def _Run(self):
        #Update all game instances
        completedGames = []
        
        for (guid, game) in self.Games.items():
            if game.Complete:
                completedGames.append(guid)
            elif not game.Paused:
                try:
                    game.Update(0)
                except:
                    log.info("TicTacToeManagerApplication game had an exception during Update(). Killing that instance.")
                    game.Complete = True                    

        for guid in completedGames:            
            self.StopGame(guid)    
                
    def StartGame(self):
        game = Game(self)
        log.info("TicTacToeManagerApplication starting game %s" % game.GUID)
        self.Games[game.GUID] = game
        return "gameGUID|" + game.GUID

    def StopGame(self, guid):
        log.info("TicTacToeManagerApplication stopping game %s" % guid)
        game = self.Games.pop(guid, None)
        if not game == None:
            try:
                game.Stop()
            except:
                log.info("TicTacToeManagerApplication got an exception when stopping a game instance. Finishing it off.")
            finally:            
                del game

    def JoinGame(self, guid, playerNum='1'):
        log.info("TicTacToeManagerApplication trying to let client join game %s" % guid)
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
        self.Player1 = None
        self.Player2 = None

        self.Paused = False
        self.Complete = False

        self.Turn = 1
        self.TurnComplete = False
        #0,1,2
        #3,4,5
        #6,7,8
        self.Board = [0,0,0,0,0,0,0,0,0]
        self.Winner = 0
        
        self.CommandMap = {}
        self.CommandMap["place"] = self.PlacePiece

    def AddPlayer(self, connection, playerNum='1'):
        if playerNum == '1' and self.Player1 == None:
            log.info("TicTacToe Game %s added player 1" % self.GUID)
            self.Player1 = connection
            self.Player1.SendCommand("joinedGame|" + self.GUID + "|1")
            self.Player1.SendCommand("board|" + repr(self.Board))
        elif playerNum == '2' and self.Player2 == None:
            log.info("TicTacToe Game %s added player 2" % self.GUID)
            self.Player2 = connection
            self.Player2.SendCommand("joinedGame|" + self.GUID + "|2")
            self.Player2.SendCommand("board|" + repr(self.Board))
            
            #throttle player 2 by default, they don't go first
            self.Player2.Throttled = True
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

        self.HandleTurn()

    def SendBoardState(self):
        self.Player1.SendCommand("board|" + repr(self.Board))
        self.Player2.SendCommand("board|" + repr(self.Board))

    def GameWon(self):
        self.Complete = True
        self.Player1.SendCommand("gameOver|" + str(self.Winner))
        self.Player2.SendCommand("gameOver|" + str(self.Winner))

    def GameDraw(self):
        self.Complete = True
        self.Player1.SendCommand("gameOver|0")
        self.Player2.SendCommand("gameOver|0")

    def NotifyPiecePlaced(self, position, player):
        self.Player1.SendCommand("placed|" + str(position) + "|" + str(player))
        self.Player2.SendCommand("placed|" + str(position) + "|" + str(player)) 
    
    def HandleTurn(self):
        if self.Turn == 1:
            self.ProcessTurn(self.Player1)
            if self.TurnComplete:
                self.Player1.Throttled = True
                self.Player2.Throttled = False
                self.Turn = 2
                self.TurnComplete = False
                self.SendBoardState()
        else:
            self.ProcessTurn(self.Player2)
            if self.TurnComplete:
                self.Player2.Throttled = True
                self.Player1.Throttled = False                
                self.Turn = 1
                self.TurnComplete = False                
                self.SendBoardState()

    def ProcessTurn(self, connection):       
        try:
            receivedCommand = connection.GetNextCommand()            
                
            if receivedCommand != None:
                commandResult = self.ProcessCommand(receivedCommand)
                
                if commandResult != None:
                    connection.SendCommand(commandResult)
        except:
            pass

    def ProcessCommand(self, command):
        parts = command.split('|')
    
        if parts[0] in self.CommandMap:
            args = parts[1:]
            result = self.CommandMap[parts[0]](*args)
            log.info('TicTacToe instance - Command %s returned %s' % (command, result))
            return result
        else:
            log.info('TicTacToe instance - Unknown command %s' % (command))
            return None        

    def CheckRow(self, a, b, c):
        x = self.Board[a] + self.Board[b] + self.Board[c]
        if x == 9:
            self.Winner = 1
            return True
        elif x == 15:
            self.Winner = 2
            return True
        else:
            return False

    def PlacePiece(self, position):
        pos = int(position)
        if pos >= 0 and pos <= 8:
            if self.Board[pos] == 0:
                if self.Turn == 1:
                    #player 1 places 3's
                    self.Board[pos] = 3
                    self.NotifyPiecePlaced(pos, 1)
                else:
                    #player 2 places 5's
                    self.Board[pos] = 5
                    self.NotifyPiecePlaced(pos, 2)

                self.TurnComplete = True

                #Win?
                if self.CheckRow(0, 1, 2) or self.CheckRow(3, 4, 5) or self.CheckRow(6, 7, 8) or self.CheckRow(0, 3, 6) or self.CheckRow(1, 4, 7) or self.CheckRow(2, 5, 8) or self.CheckRow(0, 4, 8) or self.CheckRow(2, 4, 6):            
                    self.GameWon()
                #Draw? Lowest possible full board count is 5*3 + 4*5
                elif reduce(lambda x, y: x + y, self.Board) >= 35:
                    self.GameDraw()
