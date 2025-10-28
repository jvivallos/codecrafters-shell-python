import subprocess
import shlex

class ExecutableCommand:

    def __init__(self, command, parameters):
        self.command = command
        self.parameters = parameters

    def execute(self):
        cmd = f"{self.command}" + (f" {self.parameters}" if self.parameters is not None else "")
        args = shlex.split(cmd)
        subprocess.run(args)