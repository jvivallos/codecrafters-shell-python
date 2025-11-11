import os
import subprocess
import shlex

from app.command_util import RedirectUtil

class ExecutableCommand:

    def __init__(self, command, parameters):
        self.command = command
        self.parameters = parameters

        

    def execute(self, input = None):
        cmd = f"{self.command}" + (f" {self.parameters}" if self.parameters is not None else "")
        args = shlex.split(cmd)
        output_file = None
        redirect = RedirectUtil.is_stdout_redirect(args)
        redirect_stderr = RedirectUtil.is_stderr_redirect(args)
        if redirect[0]:
            mode = "w" if redirect[1] in ('1>', '>') else "a" 
            with open(args[len(args) - 1], mode) as output_file:
                args.remove(redirect[1])
                args.remove(args[len(args) - 1])
                subprocess.run(args=args, stdout=output_file)
        elif redirect_stderr[0]:
            #os.system(f"{self.command} {self.parameters}")
            try:
                mode = "w" if redirect_stderr[1] in ('2>') else "a" 
                with open(args[len(args) - 1], mode) as err_file:
                    args.remove(redirect_stderr[1])
                    args.remove(args[len(args) - 1])
                    subprocess.run(args=args, stderr=err_file)
            except Exception as e:
                print(f"The run has failed: {e}")
        else:
            subprocess.run(args=args, input=input)

    def execute_and_return(self, input):
        subprocess.run(args=input,
                         shell=True)
        '''
        cmd = f"{self.command}" + (f" {self.parameters}" if self.parameters is not None else "")
        args = shlex.split(cmd)
        process = subprocess.Popen(args=args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output = None
        try:
            output, errors = process.communicate(input=input, timeout=1)
        except subprocess.TimeoutExpired:
            pass

        return output
        '''