import os
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
            with open(args[len(args) - 1], "w") as output_file:
                if '>' in args:
                    args.remove('>')
                else:   
                    args.remove('1>')
                args.remove(args[len(args) - 1])
                subprocess.run(args=args, stdout=output_file)
        elif '2>' in args:
            os.system(f"{self.command} {self.parameters}")
            # with open(args[len(args) - 1], "w") as err_file:
            #     args.remove('2>')
            #     args.remove(args[len(args) - 1])
            #     if 'cat' in args:
            #         subprocess.run(args=args)
            #     subprocess.run(args=args, stderr=err_file)
        else:
            subprocess.run(args=args)