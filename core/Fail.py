from colors import color
import sys

def fail(message, line):
    print(color("\nError: \n\t" + message + "\n\nLine of failure:\n\t" +
                line, fg="red"))
    sys.exit(1)
    