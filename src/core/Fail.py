from colors import color
import sys


def fail(message, error_type, line):
    print(color("\n" + error_type + ":\n\t" + message + "\n\nLine where failure occured:\n\t" +
                line, fg="red"))
    sys.exit(1)
    