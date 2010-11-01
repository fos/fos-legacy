from application import *
from connection import *

import time
import datetime
import random
random.seed(12345)

def Instantiate(appName):
    timeApp = TimeApplication(appName)
    return timeApp

class TimeApplication(Application):
    def __init__(self, name):
        Application.__init__(self, name)

        self.CommandMap["time"] = self.GetTime

    def AddClient(self, connection):
        verified = Application.AddClient(self, connection)

        if verified:
            #temp fun: send a random number to client
            randomNum = random.randint(0, 15)
            connection.SendCommand( "random|" + str(randomNum))

        return verified

    def Run(self):
        log.info("TimeApplication now running.")

        Application.Run(self)

        log.info("TimeApplication DONE running.")

    def GetTime(self):
        return "time|" + str(time.time())
