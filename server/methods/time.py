from datetime import datetime
import utilities as Utilities


def getTime():
    # Variable Definition
    response = None
    status = None

    # Code Section
    try:
        response = str(datetime.now().time())
        status = True
    except:
        response = "Error reading time"
        status = False
    finally:
        return Utilities.getResponseObject(status, response)



