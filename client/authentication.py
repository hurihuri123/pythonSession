# Local DLLs
import utilities as Utilities

class ClientAuth:
    def __init__(self):
        # Defaults login info
        self.userName       = "huri"
        self.password       = 1234
        self.registration   = "Register:"
        self.login          = "Login:"

    def getAuthMsg(self):
        msg = self.login + self.userName + " " + str(self.password)
        return msg

    def getUserName(self):
        return self.userName