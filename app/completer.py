import readline

class Completer:
    COMMANDS = ["echo", "exit"]

    def __init__(self):
        self._setup_readline()

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

    def _completer(self, text, state):
        """
        Called repeatedly by readline until it returns None.
        text: the current word being completed
        state: an integer (0, 1, 2, …) for successive matches
        """
        options = [cmd for cmd in self.COMMANDS if cmd.startswith(text)]
        if state < len(options):
            return options[state] + " "
        return None
