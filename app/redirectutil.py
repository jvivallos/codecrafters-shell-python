class RedirectUtil:

    @staticmethod
    def _is_stdout_redirect(args)->tuple:
        command_set = {'>', '1>', '1>>', '>>'}.intersection(args)
        
        result = None
        for command in command_set:
            result = command
        
        if(len(command_set) > 0):
            return (True, result)
        else:
            return (False, None)