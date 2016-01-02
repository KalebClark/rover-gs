# 0MQ Control client

import sys
sys.path.append('/opt/rover/lib')
import zmq
import json
from gamepad import gamepad

class ControlClient(object):
    
    serverIP    = '192.168.1.190'
    serverPORT  = '5555'
    payload     = {}

    def __init__(self):
        # Connect to Server
        self.connectToServer()

        self.poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)

    def connectToServer(self):
        # Establish connection to rover
        print("Connecting to: %s:%s" % (self.serverIP, self.serverPORT))
        self.context = zmq.Context()
        self.socket  = self.context.socket(zmq.REQ)
        try:
            self.socket.connect("tcp://"+self.serverIP+":"+self.serverPORT)
        except:
            print("Connection to %s:%s failed..." % (self.serverIP, self.serverPORT))

    def send(self):
        self.payload['controls'] = gamepad.get()
        self.payload['telem'] = {'foo': 'bar'}
        try:
            self.socket.send(json.dumps(self.payload), zmq.NOBLOCK)
            print("SUCCESS!!")
        except:
            print("FAILED!!!")

        ack = self.socket.recv()


control = ControlClient()
while True:
    control.send()

