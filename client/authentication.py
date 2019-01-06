import hashlib
# Local DLLs
import utilities as Utilities

class ClientAuth:
    def __init__(self):
        self.userName       = "hurs"
        self.infoFileName   = "info.txt"
        self.registration   = "Register:"
        self.login          = "Login:"
        self.authOptions    = [
            "Registration",
            "Login" ,
            "Cookies"
        ]


    def getAuthMsg(self):
        # Variable Definition
        optionMessage   = self.authOptionsToString() # Get auth msg
        selectedOption  = int(raw_input(optionMessage)) # Assuming the input is correct

        # Code Section
        if(selectedOption == 3):
            info = self.readInfoFromCookies()
            selectedOption = self.login
        else:
            info = self.getInfoFromClient()
            if(selectedOption == 2):
                selectedOption = self.login
            else:
                selectedOption = self.registration

        return selectedOption + info


    def getUserName(self):
        return self.userName

    def authOptionsToString(self):
        # Variable Definition
        optionMessage = "Choose authentication options: \n"
        # Code Section
        for index, option in enumerate(self.authOptions):
            optionMessage += str(index + 1) + " - " + option + "\n"
        return optionMessage

    def readInfoFromCookies(self):
        # Variable Definition
        infoFile = None

        # Code Section
        try:
            infoFile = open(self.infoFileName, "r")
        except:
            Utilities.logger("Couldn't find cookies file")
            return self.getAuthMsg()

        data = infoFile.read()
        infoFile.close()
        return data


    def getInfoFromClient(self):
        # Variable Definition
        userName    = raw_input("Enter username")
        password    = raw_input("Enter password")
        password    = hashlib.md5(password).hexdigest() # MD5 the password

        # Code Section
        self.userName = userName
        loginInfo = userName + " " + password

        # Save info to cookies file
        file = open(self.infoFileName,"w")
        file.write(loginInfo)
        file.close()

        return loginInfo
