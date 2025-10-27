class BuiltinCommand:
    def __init__(self, command:str, parameters:str):
        self.command = command
        self.parameters = parameters

    def execute(self):
        if self.command == "echo":
            print(self.parameters)

    @staticmethod 
    def is_builtin(command):
        #print(command in ["echo"])
        return command in ["echo"]