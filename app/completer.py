import os
import readline

class Completer:
    COMMANDS = ["exit", "history"]

    def __init__(self):
        self._load_Commands()
        self._setup_readline()
        

    def _load_Commands(self):
        path_value = os.environ.get("PATH")
        all_exec = list()
        for directory in path_value.split(os.pathsep):
            try:
                all_exec = all_exec + list(os.listdir(directory))
            except Exception as e:
                pass
        self.COMMANDS = self.COMMANDS + all_exec

    def _setup_readline(self):
        # Detect libedit vs GNU readline
        doc = readline.__doc__ or ""
        if "libedit" in doc:
            # macOS default
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
        readline.set_completer(self._completer)
        readline.set_completer_delims(" \t\n")  # Control word delimiters
        readline.set_auto_history(True)

    def _completer(self, text, state):
        """
        Called repeatedly by readline until it returns None.
        text: the current word being completed
        state: an integer (0, 1, 2, …) for successive matches
        """
        options = [cmd for cmd in self.COMMANDS if cmd.startswith(text)]
        if state < len(options):
            return options[state] + (" " if len(options) == 1 else "")
        return None

    @staticmethod
    def change_history_file(filename):
        readline.read_history_file(filename)