import shutil
import os
import shlex

from app.command_util import RedirectUtil

class BuiltinCommand:
    def __init__(self, command:str, parameters:str):
        self.command = command
        self.parameters = parameters
        self.stdout_redirect_commands = {'>', '1>', '1>>', '>>'}

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

    def execute(self):
        if self.command == "echo":
            self._echo()
        elif self.command == "type":
            self._type()
        elif self.command == "pwd":
            print(os.path.abspath("."))
        elif self.command == "cd":
            self._cd()

    def _string_escape(self, s, encoding='utf-8'):
        return (s.encode('latin1')         # To bytes, required by 'unicode-escape'
             .decode('unicode-escape') # Perform the actual octal-escaping decode
             .encode('latin1')         # 1:1 mapping back to bytes
             .decode(encoding))

    @staticmethod 
    def is_builtin(command):
        #print(command in ["echo"])
        return command in ["echo", "exit", "type", "pwd", "cd"]