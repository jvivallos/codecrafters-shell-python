import subprocess
import os
import sys
import signal
import time
import shutil

def make_line_buffered(cmd):
    """Wrap a command with stdbuf or unbuffer if available."""
    # Try GNU coreutils stdbuf first (Homebrew provides it as gstdbuf on macOS)
    for candidate in ("stdbuf", "gstdbuf"):
        if shutil.which(candidate):
            return [candidate, "-oL"] + cmd

    # Try expect's unbuffer
    if shutil.which("unbuffer"):
        return ["unbuffer"] + cmd

    # Fallback — just use the command itself
    return cmd


def run_pipeline(commands):
    """Run a two-stage pipeline like cmd1 | cmd2 and stream output live."""
    # Wrap each command for line buffering if possible
    cmd1 = make_line_buffered(commands[0])
    cmd2 = make_line_buffered(commands[1])

    p1 = subprocess.Popen(
        cmd1,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    p2 = subprocess.Popen(
        cmd2,
        stdin=p1.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    # Close parent's copy of the first pipe to propagate EOF
    p1.stdout.close()

    try:
        for line in p2.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        p2.stdout.close()
        p2.wait()

        # Give tail a moment to flush and clean up
        time.sleep(0.1)
        if p1.poll() is None:
            os.kill(p1.pid, signal.SIGPIPE)
            try:
                p1.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                p1.terminate()


if __name__ == "__main__":
    run_pipeline([
        ["tail", "-f", "/tmp/bar/file-36"],
        ["head", "-n", "5"]
    ])
