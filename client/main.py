import socket

# Local DLLs
import utilities as Utilities
import authentication as Auth

class Client:
    def __init__(self, serverIP, serverPort):
        # Variable Definition
        self.clientFD   = None
        self.serverIP   = serverIP
        self.serverPort = serverPort

        # Code Section
        self.initClientSocket()
        # TODO - get auth message
        # self.clientFD.send("Register:huri 1234")
        self.clientActions()


    def initClientSocket(self):
        # Code Section
        self.clientFD = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Create socket using Ipv4 family and TCP protocol
        self.clientFD.connect((self.serverIP, self.serverPort))          # Connect to remote server
        Utilities.logger('Connected Successfully')

    def clientActions(self):
        # Variable Definitions
        possibleActions = self.receive(self.clientFD)  # Receive actions list

        # Code Section
        while(True):
            Utilities.logger(possibleActions)
            action = raw_input("Please choose action \n")   # Get action from user
            self.send(action)                               # Send action to server
            response = self.receive(self.clientFD)          # Receive action response
            Utilities.logger(response)                      # Print response


    def send(self, data):
        self.clientFD.send(data)
        Utilities.logger("Sent : " + str(data))

    def receive(self, clientFD):
        return clientFD.recv(1024)


client = Client('127.0.0.1', 8080)