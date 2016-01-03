#
# kcRover Control CLIENT
# LOC: Ground Station
# IP: 192.168.1.180
#
# Control Client
# Sends control and telmetry from ground station
import sys
#sys.path.append('/opt/rover/lib')
import time
import zmq
import json
#from gamepad import gamepad

class ControlClient(object):
    
    #serverIP   = '192.168.1.190'
    #serverPORT = '5550'
    #request_timeout = 2500
    #request_retries = 10
    sequence = 0

    def __init__(self, serverIP, serverPORT, request_timeout=2500, request_retries=10):
        self.serverIP = serverIP
        self.serverPORT = serverPORT
        self.request_timeout = request_timeout
        self.request_retries = request_retries

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

    def send(self, payload):
        retries_left = self.request_retries
        sequence = 0

        while retries_left:
            # Prepare sequence int
            sequence += 1
            seq = sequence

            print("I: Sending sequence # (%s)" % seq)
            
            # Build payload
            payload.update({'seq': seq})

            # Send the request
            self.socket.send(json.dumps(payload))

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

                    print("I: Reconnecting and resending sequence # (%s)" % seq)
                    # RE-Establish connection to server and resend.
                    self.connect()
                    self.socket.send(json.dumps(payload))


    def receive(self):
        print "START RECEIVE"
        try:
            message = self.socket.recv()
            return message
        except:
            print("FAIL")

