import subprocess
import time

# First process: tail -f
p1 = subprocess.Popen(
    ["tail", "-f", "/tmp/bar/file-36"],
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL,  # hide tail’s stderr noise
    text=True
)

# Second process: head -n 5
p2 = subprocess.Popen(
    ["head", "-n", "5"],
    stdin=p1.stdout,
    stdout=subprocess.PIPE,
    text=True
)

# Close parent's reference to the pipe
p1.stdout.close()

# Read from head (it will exit after 5 lines)
output, _ = p2.communicate()

print(output, end="")

# Give tail a tiny moment to flush any pending writes
time.sleep(0.1)

# Terminate tail if it’s still running
if p1.poll() is None:  # still alive
    p1.terminate()
    try:
        p1.wait(timeout=1)
    except subprocess.TimeoutExpired:
        p1.kill()

# Done
