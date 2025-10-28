import shutil

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

    def execute(self):
        if self.command == "echo":
            print(self.parameters)
        elif self.command == "type":
            self._type()

    @staticmethod 
    def is_builtin(command):
        #print(command in ["echo"])
        return command in ["echo", "exit", "type"]