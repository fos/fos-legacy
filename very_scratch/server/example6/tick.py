import util
import time

def tick(to_read, to_write, to_error, scope):
    #do something
    print "tick"
    for socko in to_write:
        #util.ws_send(socko, scope.setdefault("last_message", ""))
        util.ws_send(socko, time.clock())