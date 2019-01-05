# The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
from subprocess import PIPE, Popen
import subprocess

class CLI:
    def __init__(self):
        # Variable Definition
        self.currentWorkingDirectory = '/'

    def runShellCommand(self, command):
        # Code Section
        if(self.detectCdCommand(command)):
            return self.currentWorkingDirectory

        try:
            process = Popen(args=command,stdout=PIPE,shell=True,cwd=self.currentWorkingDirectory)
            result = process.communicate()[0]    # Interact with process: Send data to stdin. Read data from stdout and stderr
        except:
            result = "Bad Command"

        return result


    def detectCdCommand(self,command):
        # Code Section
        if("cd" in command):
            # Cut 'cd ' and set CWD
            self.currentWorkingDirectory = '/' + (command.split("cd ")[1])
            return True
        return False
