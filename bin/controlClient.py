#
# kcRover Control CLIENT
# LOC: Ground Station
# IP: 192.168.1.180
#
# Control Client
# Sends control and telmetry from ground station
import sys
sys.path.append('/opt/rover/lib')
import time
import zmq
import json
from gamepad import gamepad

class ControlClient(object):
    
    serverIP   = '192.168.1.190'
    serverPORT = '5550'
    payload    = {}
    request_timeout = 2500
    request_retries = 10
    sequence = 0

    def __init__(self):

        self.serverAddr = "tcp://"+self.serverIP+":"+self.serverPORT

        # Connect to Server
        self.connect()



    def connect(self):
        # Establish connection to server
        self.context = zmq.Context(1)
        self.socket  = self.context.socket(zmq.REQ)
        print("Connecting to server: %s" % self.serverAddr)
        self.socket.connect(self.serverAddr)

        # Register Poller
        self.poll = zmq.Poller()
        self.poll.register(self.socket, zmq.POLLIN)

    def send(self):
        retries_left = self.request_retries
        sequence = 0

        while retries_left:
            sequence += 1
            request = str(sequence)
            print("I: Sending (%s)" % request)

            # Send the request
            self.socket.send(request)

            expect_reply = True
            while expect_reply:
                socks = dict(self.poll.poll(self.request_timeout))
                if socks.get(self.socket) == zmq.POLLIN:
                    reply = self.socket.recv()
                    if not reply:
                        break
                    if int(reply) == sequence:
                        # SUCCESS: Server replied correctly
                        print("I: Server replied OK (%s)" % reply)
                        retries_left = self.request_retries
                        expect_reply = False
                    else:
                        # FAILURE: Server has malformed reply
                        print("E: Malformed reply from server: %s" % reply)
                else:
                    # FAILURE: Socket is confused.
                    print("W: No response from server. Retry...")
                    self.socket.setsockopt(zmq.LINGER, 0)
                    self.socket.close()
                    self.poll.unregister(self.socket)
                    retries_left -= 1
                    if retries_left == 0:
                        print("E: Server seems to be offline. Abandoning")
                        break

                    print("I: Reconnecting and resending (%s)" % request)
                    # RE-Establish connection to server and resend.
                    self.connect()
                    self.socket.send(request)


    def receive(self):
        print "START RECEIVE"
        try:
            message = self.socket.recv()
            return message
        except:
            print("FAIL")

control = ControlClient()
while True:
    control.send()

