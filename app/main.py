import sys
from app.builtin_command import BuiltinCommand
from app.command_util import PipeUtil
from app.executable_command import ExecutableCommand
from app.completer import Completer

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

def execute_piped_commands(user_input):
    input = None
    commands = PipeUtil.parse_multiple_commands(user_input)
    ExecutableCommand('hello', 'world').execute_and_return(user_input)
    '''
    for full_command in commands[0:len(commands) - 1]:
        command_parameters = parse_command(full_command)
        command = command_parameters[0]
        parameters = command_parameters[1]
        executableCommand = ExecutableCommand(command, parameters)
        buffer = executableCommand.execute_and_return(input)
        input = buffer
    
    full_command = commands[len(commands) - 1]
    command_parameters = parse_command(full_command)
    command = command_parameters[0]
    parameters = command_parameters[1]
    executableCommand = ExecutableCommand(command, parameters)
    executableCommand.execute(input if input else None)
    '''

def main():
    Completer()
    while True:
        
        user_input = input("$ ")

        if(user_input.startswith("exit 0")):
            return 0
        if(user_input == ""):
            continue
        if(PipeUtil.has_piped_commands(user_input)):
            execute_piped_commands(user_input)
            continue
        command_parameters = parse_command(user_input)
        
        command = command_parameters[0]
        parameters = command_parameters[1]
        if(BuiltinCommand.is_builtin(command)):
            builtinCommand = BuiltinCommand(command, parameters)
            builtinCommand.execute()
        else:
            try:
                executableCommand = ExecutableCommand(command, parameters)
                executableCommand.execute()
            except FileNotFoundError as e:
                print("{}: command not found".format(user_input))
            except Exception as e:
                print(e);
        


if __name__ == "__main__":
    main()
