
# Local packages
import utilities as Utilities
import sqliteDB as DB

class ServerAuth:
    def __init__(self):
        # Variable Definition
        self.dbPath         = 'db'
        self.tableName      = "users"
        self.tableColumns   = ["userName", "password"]
        self.db             = DB.sqlLiteDataBase(self.dbPath)  # Connect to the DB file
        self.initUsersTable()

        self.authOptions = {
            'Register': self.registration,
            'Login':    self.login,
            'Cookies:': 'cook'
        }

    def authenticate(self, data):
        # Variable Definition
        status  = None

        # Code Section
        Utilities.logger('Received authentication message : ' + data)
        return self.anlayzeRequest(data)


    def anlayzeRequest(self, request):
        # Variable Definition
        method, data = request.split(':')

        # Code Section
        return self.authOptions[method](data) # Execute auth method


    def registration(self, data):
        # Variable Definition
        data    = data.split(' ')       # [userName, password]

        # Test user existence
        isUserExistes = self.db.testRowExistence(self.tableName, self.tableColumns[0], data[0])
        if(isUserExistes) :
            return self.getResponseObject(False, self.userExistenceError())

        # Insert new user
        return self.insertNewUser(data)


    def insertNewUser(self, data):
        # Variable Definition
        response = None

        # Code Section
        try:
            self.db.insertRowToTable(self.tableName, data, self.tableColumns)  # Insert new row to DB
            response = self.getResponseObject(True, self.successRegist())
        except ValueError as err:
            response = self.getResponseObject(False, "Auth Faild -> " + str(err))
        finally:
            return response


    def initUsersTable(self):
        if(self.db.testTableExistence(self.tableName) == False) : # Test table existence
            self.db.createTable(self.tableName, self.tableColumns)
            Utilities.logger("Created users table")


    def login(self, data):
        # Variable Definition
        data = data.split(' ')          # [userName, password]

        # Code Section
        compareObj = {self.tableColumns[0]: data[0], self.tableColumns[1]: data[1]}

        result = self.db.testLogin(self.tableName, self.tableColumns, compareObj)

        return self.getResponseObject(True, self.dbSuccessLogin()) \
            if result else self.getResponseObject(False, self.dbFailLogin())



    # DB messages

    def dbMessages(self):
        # Variable Definition
        messages = {
            'succesfullyCreated'    : 'Registed Succesfully',
            'userAlreadyExiste'     : 'Registration Failed -> User already registered',
            'dataBaseError'         : 'Internal DB Error',
            'successLogin'          : 'Logged in succesfully',
            'failLogin'             : 'Wrong password or userName'
        }

        # Code Section
        return messages

    def userExistenceError(self):
        return self.dbMessages()['userAlreadyExiste']

    def successRegist(self):
        return self.dbMessages().get('succesfullyCreated')

    def dbErrorMessage(self):
        return self.dbMessages().get('dataBaseError')

    def dbSuccessLogin(self):
        return self.dbMessages().get('successLogin')

    def dbFailLogin(self):
        return self.dbMessages().get('failLogin')

    def getResponseObject(self, status, message):
        return {"status": status, "message": message}