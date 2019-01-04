import socket
import threading
import Cookie

# Local DLLs
import utilities as Utilities
import authentication as Auth

class Server:
    def __init__(self, port):
        # Variable Definition
        self.serverFD       = None
        self.serverThread   = None
        self.clientThreads  = []
        self.auth           = Auth.ServerAuth()


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
        authMessage = clientFD.recv(1024)
        self.auth.authenticate(authMessage, self.auth)


        # action = self.receive(clientFD) # Receive action

        # while(True):
        #     action = clientFD.recv(1024)  # Receive action
        #     # action = self.receive(clientFD) # Receive action
        #     Utilities.logger(action)
        #     # self.performAction(clientFD)    # Perform action


    def send(clientFD, data):
        clientFD.send(data)
        Utilities.logger("Sent : " + str(data))



server = Server(8080) # Init server socket
