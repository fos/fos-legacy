from application import *
from connection import *

import time
import datetime


def Instantiate(appName='admin'):
    adminApp = AdminApplication(appName)
    return adminApp

class AdminApplication(Application):
    def __init__(self, name='admin'):
        Application.__init__(self, name)

        self.CommandMap["startApp"] = self.StartApp
        self.CommandMap["stopApp"] = self.StopApp
        self.CommandMap["getStats"] = self.GetStats

    def Run(self):
        log.info("AdminApplication now running.")

        Application.Run(self)

        log.info("AdminApplication DONE running.")

    def StartApp(self):
        pass

    def StopApp(self):
        pass

    def GetStats(self):
        pass
