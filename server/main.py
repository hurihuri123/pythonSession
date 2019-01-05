import socket
import threading
import struct
# Local packages
import utilities as Utilities
from server.methods import *


class Server:
    def __init__(self, port):
        # Variable Definition
        self.serverFD       = None
        self.serverThread   = None
        self.clientThreads  = []
        # self.auth           = Auth.ServerAuth() - create int __init__.py

        self.actions = [
            {"TIME":        getTimeMethod},
            {"NAME":        getComputerName},
            {"EXIT":        self.closeConnection},
            {"SCREENSHOT":  screenObject.CaptureScreenShot},
            {"CLI":         self.handleCLIrequests},
        ]

        # Code Section
        self.initServerSocket(port)


    def initServerSocket(self, port):
        self.serverFD = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # Create socket using Ipv4 family and TCP protocol
        self.serverFD.bind(('127.0.0.1', port)) # Bind socket with specific address & port
        self.serverFD.listen(10)                # Listen & Set pending queue length
        Utilities.logger("Server is listening...")

        t = threading.Thread(target = self.handleNewConnections).start() # Start connections handler thread
        self.serverThread = t                       # Store server thread

    def handleNewConnections(self):
        # Code Section
        while(True):
            client, address = self.serverFD.accept()     # Accept new connection
            Utilities.logger("Accepted new connection from " + address[0])

            t = threading.Thread(target = self.handleConnection, args = (client,)).start() # Start connection handler thread
            self.clientThreads.append(t)

    def handleConnection(self, clientFD):
        # Code Section
        # authMessage = clientFD.recv(1024)
        # self.auth.authenticate(authMessage, self.auth)

        self.send(clientFD, self.actionsToString())                     # Send actions list to client
        while(True):
            actionIndex = self.receive(clientFD)                        # Receive action from client
            response = self.performAction(clientFD, int(actionIndex))   # Perform action
            self.send(clientFD, response)


    def performAction(self, clientFD, actionIndex):
        # Variable Definition
        actionDict  = self.actions[actionIndex]
        dictKey     = next(iter(actionDict)) # Get first dict key

        # Code Section
        if(dictKey == "CLI"):
            return actionDict[dictKey](clientFD)
        return actionDict[dictKey]()


    def actionsToString(self):
        # Variable Definition
        string = ''

        # Code Section
        for index, action in enumerate(self.actions): # Enumrate is used to get the element & the index
            for key in action:
                string +=  str(index) + ' - ' + key + '\n'

        return string


    def send(self, clientFD, data):
        # Prefix each message with a 4-byte length (network byte order)
        data = struct.pack('>I', len(data)) + data

        clientFD.sendall(data)      # Send loop until all bytes successfully delivered
        Utilities.logger("Sent" + str(len(data)) + " bytes")

    def receive(self, clientFD):
        return clientFD.recv(1024)

    def closeConnection(self):
        # TODO - kill/stop thread & close socket
        # Code Section
        return Utilities.getResponseObject(True, "Bye Bye")

    def handleCLIrequests(self, clientFD):
        # Variable Definition
        CLIobject               = CLI.CLI()       # Init CLI
        command                 = None
        welcomeMsg              = "Welcome to Huri's CLI\n"
        goodByeMsg              = "GoodBye \n"
        waitingforCommandMsg    = "Please write a command or type 'exit' to quit CLI...\n"

        # Code Section
        self.send(clientFD, welcomeMsg)
        while(command != "exit"):
            self.send(clientFD, waitingforCommandMsg)
            command = self.receive(clientFD)
            result  = CLIobject.runShellCommand(command)
            self.send(clientFD, result)

        self.send(clientFD,goodByeMsg)






server = Server(8080) # Init server socket
