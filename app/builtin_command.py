class BuiltinCommand:
    def __init__(self, command:str, parameters:str):
        self.command = command
        self.parameters = parameters

    def execute(self):
        if self.command == "echo":
            print(self.parameters)
        elif self.command == "type":
            if BuiltinCommand.is_builtin(self.parameters):
                print(f"{ self.parameters } is a shell builtin")
            else:
                print(f"{ self.parameters } not found")

    @staticmethod 
    def is_builtin(command):
        #print(command in ["echo"])
        return command in ["echo", "exit", "type"]