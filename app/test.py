import os
from pathlib import Path
import sys
import readline


def list_folder(path):
    """
    Lists folder contents
    """

    path_value = os.environ.get("PATH")
    all_exec = list()
    for directory in path_value.split(os.pathsep):
        #print(directory)
        try:
            all_exec = all_exec + list(os.listdir(directory))
        except Exception as e:
            pass
    
    #print(len(all_exec))
    return all_exec
    
    '''
    print(list(os.listdir(directory)))

    if path.startswith(os.path.sep):
        # absolute path
        basedir = os.path.dirname(path)
        contents = os.listdir(basedir)
        # add back the parent
        contents = [os.path.join(basedir, d) for d in contents]
    else:
        # relative path
        contents = os.listdir(os.curdir)
    return contents
    '''


def completer(text, state):
    """
    Our custom completer function
    """
    options = [x for x in list_folder(text) if x.startswith(text)]
    return options[state]

readline.set_completer(completer)

if sys.platform == 'darwin':
    # Apple uses libedit.
    readline.parse_and_bind("bind -e")
    readline.parse_and_bind("bind '\t' rl_complete")
else:
    # Some tweaks for linux
    readline.parse_and_bind('tab: complete')
    readline.set_completer_delims(' \t\n`~!@#$%^&*()-=+[{]}\\|;:\'",<>?')


### Try out the stuff:
while True:
    last_string = input('? ')
    print ('Last input:', last_string)