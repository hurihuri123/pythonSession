# Local DLLs
import utilities as Utilities

class ClientAuth:
    def __init__(self):
        self.userName       = "hurs"
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
        return "huri 1234"

    def getInfoFromClient(self):
        # Variable Definition
        userName    = raw_input("Enter username")
        password    = raw_input("Enter password")

        # Code Section
        self.userName = userName
        return userName + " " + password
