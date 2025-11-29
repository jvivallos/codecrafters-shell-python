import os
import readline

class HistoryManager:
    def __init__(self, file_path='~/.python_history'):
        # Use HISTFILE if set, otherwise default
        env_path = os.environ.get("HISTFILE")
        self.file_path = os.path.expanduser(env_path) if env_path else os.path.expanduser(file_path or "~/.python_history")
        self.commands = []
        self.last_saved_index = 0  # Tracks commands already written to file
        self.load(self.file_path)

    # -----------------------------
    # Core syncing
    # -----------------------------
    def sync_last_item(self):
        """Sync the last readline entry into self.commands."""
        length = readline.get_current_history_length()
        if length == 0:
            return
        last = readline.get_history_item(length)
        if last is not None and (not self.commands or self.commands[-1] != last):
            self.commands.append(last)

    # Optional: sync entire readline history
    def sync_all(self):
        new = []
        length = readline.get_current_history_length()
        for i in range(1, length + 1):
            item = readline.get_history_item(i)
            if item is not None:
                new.append(item)
        self.commands = new

    # -----------------------------
    # File operations
    # -----------------------------
    def load(self, file_path):
        """Read a history file and append its lines into history."""
        if os.path.exists(file_path):
            with open(file_path, encoding="utf-8") as f:
                for line in f:
                    cmd = line.rstrip("\n")
                    if cmd:
                        self.commands.append(cmd)
                        readline.add_history(cmd)

    def save(self, file_path=None):
        """Overwrite a history file with all commands."""
        path = file_path or self.file_path
        self.sync_last_item()
        with open(path, "w", encoding="utf-8") as f:
            for cmd in self.commands:
                f.write(cmd + "\n")
        self.last_saved_index = len(self.commands)

    def append_to_file(self, file_path=None):
        """Append all unsaved commands to the file."""
        path = file_path or self.file_path
        self.sync_last_item()
        new_commands = self.commands[self.last_saved_index:]
        if not new_commands:
            return
        with open(path, "a", encoding="utf-8") as f:
            for cmd in new_commands:
                f.write(cmd + "\n")
        self.last_saved_index = len(self.commands)

    # -----------------------------
    # Accessors
    # -----------------------------
    def all(self):
        return self.commands

    def tail(self, n):
        return self.commands[-n:]
