import sys
from app.builtin_command import BuiltinCommand

def parse_command(user_input: str):
    if user_input.count(' ') == 0:
        #print("none")
        return user_input, None

    parsed = user_input.partition(" ")
    
    if parsed[1] and parsed[2]:
        #print("command with parameters")
        return parsed[0], parsed[2]
    else:
        return None

def main():
    
    while True:
        sys.stdout.write("$ ")
        user_input = input()

        if(user_input.startswith("exit 0")):
            return 0
        command_parameters = parse_command(user_input)
        
        command = command_parameters[0]
        parameters = command_parameters[1]
        if(BuiltinCommand.is_builtin(command)):
            builtinCommand = BuiltinCommand(command, parameters)
            builtinCommand.execute()
        else:
            print("{}: command not found".format(user_input))
        


if __name__ == "__main__":
    main()
