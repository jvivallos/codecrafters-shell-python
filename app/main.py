import sys
from app.builtin_command import BuiltinCommand
from app.command_util import PipeUtil
from app.executable_command import ExecutableCommand
from app.completer import Completer
from app.history_manager import HistoryManager

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


def main():
    Completer()
    history_manager = HistoryManager()

    while True:
        user_input = input("$ ")

        history_manager.sync_last_item()

        if user_input.startswith("exit"):
            return 0

        if user_input == "":
            continue

        if PipeUtil.has_piped_commands(user_input):
            execute_piped_commands(user_input)
            continue

        command, parameters = parse_command(user_input)

        if BuiltinCommand.is_builtin(command):
            builtin = BuiltinCommand(command, parameters, history_manager)
            builtin.execute()         # <-- safe now
        else:
            try:
                ExecutableCommand(command, parameters).execute()
            except FileNotFoundError:
                print(f"{user_input}: command not found")
            except Exception as e:
                print(e)

        
        


if __name__ == "__main__":
    main()
