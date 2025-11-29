import shutil
import os
import shlex
import readline

from app.command_util import RedirectUtil
from app.completer import Completer
from app.history_manager import HistoryManager

class BuiltinCommand:
    def __init__(self, command:str, parameters:str, history_manager:HistoryManager):
        self.command = command
        self.parameters = parameters
        self.stdout_redirect_commands = {'>', '1>', '1>>', '>>'}
        self.history_manager = history_manager

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

    def _writeToFile(self, filepath, content, mode='w'):
        with open(filepath, mode) as file:
            file.write(content)

    def _echo(self):
        params = shlex.split(self.parameters)

        redirect = RedirectUtil.is_stdout_redirect(params)
        redirect_stderr = RedirectUtil.is_stderr_redirect(params)
        if redirect[0]:
            mode = "w" if redirect[1] in ('1>', '>') else "a"
            if '-e' in params:
                params.remove('-e')
            self._writeToFile(params[2], f"{self._string_escape(params[0])}\n", mode)
        elif redirect_stderr[0]:
            mode = "w" if redirect_stderr[1] in ('2>') else "a" 
            self._writeToFile(params[2], "", mode)
            print(f"{params[0]}")
        else:
            print(' '.join(params))


    def _history(self):
        args = None
        if self.parameters:
            args = shlex.split(self.parameters)

        # No args: show all history
        if not args:
            for i, cmd in enumerate(self.history_manager.all(), start=1):
                print(f"{i} {cmd}")
            return

        # history N
        if len(args) == 1 and args[0].isdigit():
            n = int(args[0])
            entries = self.history_manager.tail(n)
            start_index = len(self.history_manager.all()) - len(entries) + 1
            for i, cmd in enumerate(entries, start=start_index):
                print(f"{i} {cmd}")
            return

        # history -r file   (read)
        if len(args) == 2 and args[0] == "-r":
            self.history_manager.load(args[1])
            return

        # history -w file   (write)
        if len(args) == 2 and args[0] == "-w":
            self.history_manager.save(args[1])
            return



    # def _history(self):
    #     user_length = None
    #     length = readline.get_current_history_length() + 1
    #     if self.parameters:
    #         params = shlex.split(self.parameters)
    #         user_length = params[0]

    #     if user_length != None and user_length.isnumeric():
    #         user_length = int(user_length)

    #         if user_length > length:
    #             user_length = length - 1

    #         for i in range(length - user_length, length):
    #             print(f"{ i } { readline.get_history_item(i) }")
    #     elif self.parameters and params[0] and params[0] == '-r' and params[1]:
    #         Completer.change_history_file(params[1])
    #     else:
    #         for i in range(1, length):
    #             print(f"{ i } { readline.get_history_item(i) }")
        

    def execute(self):
        if self.command == "echo":
            self._echo()
        elif self.command == "type":
            self._type()
        elif self.command == "pwd":
            print(os.path.abspath("."))
        elif self.command == "cd":
            self._cd()
        elif self.command == "history":
            self._history()

    def _string_escape(self, s, encoding='utf-8'):
        return (s.encode('latin1')         # To bytes, required by 'unicode-escape'
             .decode('unicode-escape') # Perform the actual octal-escaping decode
             .encode('latin1')         # 1:1 mapping back to bytes
             .decode(encoding))

    @staticmethod 
    def is_builtin(command):
        #print(command in ["echo"])
        return command in ["echo", "exit", "type", "pwd", "cd", "history"]