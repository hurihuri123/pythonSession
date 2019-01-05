import socket
import threading
import struct
import time as PythonTime
from threading import Lock

# Local packages
import utilities as Utilities
from server.methods import *
from server.auth import *


class Server:
    def __init__(self, port):
        # Variable Definition
        self.serverFD           = None
        self.keepAliveFD        = None
        self.serverThread       = None
        self.keepAliveThread    = None
        self.clients            = []
        self.keepAliveClients   = []
        self.mutex              = Lock()

        self.actions = [
            {"TIME":            getTimeMethod},
            {"NAME":            getComputerName},
            {"EXIT":            self.closeConnection},
            {"SCREENSHOT":      screenObject.CaptureScreenShot},
            {"CLI":             self.handleCLIrequests},
            {"StopKeepAlive":   self.stopKeepAlive}
        ]

        # Code Section
        self.initServerSocket(port)
        self.initKeepAliveServer(port + 1)


    def initServerSocket(self, port):
        self.serverFD = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # Create socket using Ipv4 family and TCP protocol
        self.serverFD.bind(('127.0.0.1', port)) # Bind socket with specific address & port
        self.serverFD.listen(10)                # Listen & Set pending queue length
        Utilities.logger("Server is listening...")

        t = threading.Thread(target = self.handleNewConnections).start()    # Start connections handler thread
        self.serverThread = t                                               # Store server thread

    def initKeepAliveServer(self, port):
        self.keepAliveFD = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # Create socket using Ipv4 family and TCP protocol
        self.keepAliveFD.bind(('127.0.0.1', port)) # Bind socket with specific address & port
        self.keepAliveFD.listen(10)                # Listen & Set pending queue length
        Utilities.logger("KeepAlive server is listening...")

        t = threading.Thread(target=self.handleKeepAliveConnections).start()    # Start connections handler thread
        self.keepAliveThread = t                                                # Store server thread

    def handleNewConnections(self):
        # Code Section
        while(True):
            client, address = self.serverFD.accept()     # Accept new connection
            userName = self.receive(client)
            Utilities.logger("Accepted new connection from " + userName)

            t = threading.Thread(target = self.handleConnection, args = (client,)).start() # Start connection handler thread
            self.clients.append({"socket": client, "thread": t})

    def handleConnection(self, clientFD):
        # Code Section
        if(not self.authNewClient(clientFD)):
            return

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
        if(dictKey == "CLI" or dictKey == "StopKeepAlive"):
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

    def closeConnection(self):
        # Code Section
        return Utilities.getResponseObject(True, "Bye Bye")
        # TODO - pass clientFD and close his 2 sockets + threads + remove from keep alive

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

        return goodByeMsg

    def handleKeepAliveConnections(self):
        # Variable Definition

        # Code Section
        k = threading.Thread(target=self.keepAlive).start()  # Start keep alive thread

        while(True):
            client, address = self.keepAliveFD.accept()     # Accept new connection
            Utilities.logger("Accepted new keepAlive connection from " + address[0])

            self.keepAliveClients.append({"socket": client, id: "clientID"})

    def keepAlive(self):
        # Code Section
        while(True):
            for client in self.keepAliveClients:
                self.send(client["socket"], "isAlive")
            PythonTime.sleep(5)

    def stopKeepAlive(self, clientFD):
        # Code Section
        # TODO - search socket by id and delete it from list
        # self.keepAliveClients.remove({"socket": clientFD}) # Remove the client
        self.keepAliveClients = []
        return Utilities.getResponseObject(False, "Terminated keep alive")


    def authNewClient(self, clientFD):
        # Code Section
        authMessage = clientFD.recv(1024)

        self.mutex.acquire()                            # Lock Access to DB
        serverAuth = authentication.ServerAuth()        # Create auth instance
        result = serverAuth.authenticate(authMessage)   # Authenticate
        self.mutex.release()                            # Unlock Access to DB
        status = result["status"]

        self.send(clientFD, Utilities.serialize(result))

        if(not status):
            self.closeConnection()
            Utilities.logger("Authentication failed")

        return status







server = Server(8080) # Init server socket
