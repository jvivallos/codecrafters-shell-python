import shutil
import os
import shlex

class BuiltinCommand:
    def __init__(self, command:str, parameters:str):
        self.command = command
        self.parameters = parameters

    def _type(self):
        if BuiltinCommand.is_builtin(self.parameters):
            print(f"{ self.parameters } is a shell builtin")
        else:
            location = shutil.which(self.parameters)
            if location is not None:
                print(f"{self.parameters} is {location}")
            else:
                print(f"{self.parameters}: not found")

    def _cd(self):
        try:
            path = os.path.expanduser(self.parameters)
            os.chdir(path)
        except OSError:
            print(f"cd: {self.parameters}: No such file or directory")

    def _echo(self):
        text = shlex.split(self.parameters)

        print(' '.join(text))

    def execute(self):
        if self.command == "echo":
            self._echo()
        elif self.command == "type":
            self._type()
        elif self.command == "pwd":
            print(os.path.abspath("."))
        elif self.command == "cd":
            self._cd()

    @staticmethod 
    def is_builtin(command):
        #print(command in ["echo"])
        return command in ["echo", "exit", "type", "pwd", "cd"]