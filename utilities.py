import json

def logger(string):
    print(string + "\n")


def send(clientFD, data):
    clientFD.send(data)
    logger("Sent : " + str(data))


def receive(clientFD):
    return clientFD.recv(1024)

def getResponseObject(status, message):
    return serialize({"status": status, "message": message})

def serialize(data):
    return json.dumps(data) # Data structure => string

def deserialize(data):
    return json.loads(data) # String => Original data structure