import subprocess
import shlex

class ExecutableCommand:

    def __init__(self, command, parameters):
        self.command = command
        self.parameters = parameters

    def execute(self):
        cmd = f"{self.command}" + (f" {self.parameters}" if self.parameters is not None else "")
        args = shlex.split(cmd)
        output_file = None
        if '>' in args or '1>' in args:
            output_file = open(args[len(args) - 1], "w")
            if '>' in args:
                args.remove('>')
            else:   
                args.remove('1>')
            args.remove(args[len(args) - 1])
        subprocess.run(args=args, stdout=output_file)