import os
import readline

class HistoryManager:
    def __init__(self, file_path='~/.python_history'):
        self.file_path = os.path.expanduser(file_path)
        self.commands = []
        self.load(self.file_path)

    # -----------------------------
    # Core Syncing
    # -----------------------------
    def sync_last_item(self):
        """Sync the last readline entry into self.commands."""
        length = readline.get_current_history_length()
        if length == 0:
            return
        
        last = readline.get_history_item(length)
        if last is not None:
            if not self.commands or self.commands[-1] != last:
                self.commands.append(last)

    def sync_all(self):
        """(Optional) sync entire readline history if needed."""
        new = []
        length = readline.get_current_history_length()
        for i in range(1, length + 1):
            item = readline.get_history_item(i)
            if item is not None:
                new.append(item)
        self.commands = new

    # -----------------------------
    # File I/O
    # -----------------------------
    def load(self, file_path):
        """Read a history file and APPEND its lines to current history."""
        if os.path.exists(file_path):
            with open(file_path, encoding="utf-8") as f:
                for line in f:
                    cmd = line.rstrip("\n")
                    if cmd:
                        self.commands.append(cmd)
                        readline.add_history(cmd)


    def save(self, file_path=None):
        path = file_path or self.file_path
        self.sync_last_item()
        with open(path, "w", encoding="utf-8") as f:
            for cmd in self.commands:
                f.write(cmd + "\n")

    # -----------------------------
    # Public accessors
    # -----------------------------
    def all(self):
        return self.commands

    def tail(self, n):
        return self.commands[-n:]
