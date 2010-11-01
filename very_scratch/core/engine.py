#! /usr/bin/env python
from threading import Thread
import time
import scene

class Engine(Thread):

    def __init__(self):

        Thread.__init__(self)

    def run(self):
        
        sc=scene.Scene()
        sc.run()

engine = Engine()

print('starting engine ...')
engine.start()
print('engine on')

'''
while True:
	print "threa"
	time.sleep(1)
      
'''
      

