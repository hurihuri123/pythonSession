def logger(string):
    print(string + "\n")


def send(clientFD, data):
    clientFD.send(data)
    logger("Sent : " + str(data))


def receive(clientFD):
    return clientFD.recv(1024)
