import utilities as Utilities
import os


def getComputerName():
    # Variable Definition
    name = os.environ['COMPUTERNAME']

    # Code Section
    result = Utilities.getResponseObject(True, name) \
        if (name != None and name != '') \
        else Utilities.getResponseObject(False, "Error reading computer's name")

    return result
