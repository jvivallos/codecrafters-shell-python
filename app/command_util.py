import shlex

class RedirectUtil:

    @staticmethod
    def is_stdout_redirect(args)->tuple:
        command_set = {'>', '1>', '1>>', '>>'}.intersection(args)
        
        result = None
        for command in command_set:
            result = command
        
        if(len(command_set) > 0):
            return (True, result)
        else:
            return (False, None)
        
    @staticmethod
    def is_stderr_redirect(args)->tuple:
        command_set = {'2>', '2>>'}.intersection(args)
        
        result = None
        for command in command_set:
            result = command
        
        if(len(command_set) > 0):
            return (True, result)
        else:
            return (False, None)
        
class PipeUtil:

    @staticmethod
    def has_piped_commands(cmd):
        args = shlex.split(cmd)
        return '|' in args
    
    @staticmethod
    def parse_multiple_commands(cmd):
        args = shlex.split(cmd)
        commands = []
        current_command = []
        for arg in args:
            if arg == '|':
                commands.append(" ".join(current_command))
                current_command = []
            else:
                current_command.append(arg)
        if current_command: # Add any remaining elements
            commands.append(" ".join(current_command))
        return commands