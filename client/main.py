import socket
import struct
import threading
import time

# Local packages
import utilities as Utilities
from client import *
import authentication as Auth

class Client:
    def __init__(self, serverIP, serverPort):
        # Variable Definition
        self.clientFD           = None
        self.keepAliveFD        = None
        self.keepAliveThread    = None
        self.serverIP           = serverIP
        self.serverPort         = serverPort

        # Code Section
        self.initClientSocket()
        if (not self.clientAuth()):
            return
        self.initKeepAliveSokcet()
        self.clientActions()


    def initClientSocket(self):
        # Code Section
        self.clientFD = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Create socket using Ipv4 family and TCP protocol
        self.clientFD.connect((self.serverIP, self.serverPort))          # Connect to remote server
        Utilities.logger('Client socket connected Successfully')

    def initKeepAliveSokcet(self):
        self.keepAliveFD = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Create socket using Ipv4 family and TCP protocol
        self.keepAliveFD.connect((self.serverIP, self.serverPort + 1))      # Connect to remote server
        Utilities.logger('KeepAlive socket connected Successfully')
        self.keepAliveThread = threading.Thread(
            target=self.testIsAlive).start()  # Start connections handler thread

    def clientActions(self):
        # Variable Definitions
        possibleActions = self.receive(self.clientFD)  # Receive actions list

        # Code Section
        while(True):
            Utilities.logger(possibleActions)
            request = raw_input("Please choose action \n")      # Get action from user
            self.send(request)                                  # Send action to server
            response = self.receive(self.clientFD)              # Receive action response
            self.analyzeResponse(request,response)              # Analyze response


    # Socket helper functions
    def send(self, data):
        self.clientFD.send(data)
        Utilities.logger("Sent : " + str(data))

    def receive(self, clientFD):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(clientFD, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(clientFD, msglen)

    # Helper function to recv n bytes or return None if EOF is hit
    def recvall(self, clientFD, length):
        data = b''
        while len(data) < length:
            packet = clientFD.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data


    def analyzeResponse(self, request, response):
        # Variable Definition
        requests = {'3': openImage,
                    '4': self.sendCLIrequests}

        # Code Section
        return requests.get(request, self.deserializeResponse)(response)


    def deserializeResponse(self,  response):
        # Variable Definition
        response = Utilities.deserialize(response)  # Deserialize response

        # Code Section
        # Set print color according to response status
        color = PrintColors.OKGREEN if response["status"] else PrintColors.FAIL

        Utilities.logger(color + response["message"])  # Print response
        Utilities.logger(PrintColors.RESET)

        return response["status"]



    def sendCLIrequests(self, serverMessage):
        # Variable Definition
        command = None

        # Code Section
        self.CLIlogger(serverMessage)                   # Print welcome message
        while(command != "exit"):
            serverMessage = self.receive(self.clientFD) # Server waiting for input msg
            command = raw_input(serverMessage)          # Get input from client
            self.send(command)                          # Send command to server
            result = self.receive(self.clientFD)        # Receive command result
            self.CLIlogger(result)                      # Print result

        serverMessage = self.receive(self.clientFD)     # Receive goodBye msg
        self.CLIlogger(serverMessage)


    def CLIlogger(self, msg):
        # Variable Definition
        color = PrintColors.HEADER

        # Code Section
        Utilities.logger(color + msg)

    def testIsAlive(self):
        # Variable Definition
        isAlive = True
        color = PrintColors.UNDERLINE

        # Code Section
        self.keepAliveFD.settimeout(10)  # Close FD after 10 sec IDLE
        while(isAlive):
            try:
                self.keepAliveFD.recv(1024)
                Utilities.logger(color + "isAlive")
            except:
                isAlive = False
                self.exit()

    def exit(self):
        # Code Section
        self.clientFD.close()       # Close Socket
        self.keepAliveFD.close()    # Close Socket
        Utilities.logger(PrintColors.WARNING + "Connection to remote expired")

    def clientAuth(self):
        # Variable Definition
        authMsg = authInstance.getAuthMsg()

        # Code Section
        self.clientFD.send(authMsg)                 # Send Auth data
        response = self.receive(self.clientFD)      # Receive Response
        return self.deserializeResponse(response)













client = Client('127.0.0.1', 8080)