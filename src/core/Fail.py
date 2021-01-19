# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from colors import color
import sys


def fail(message, error_type, call_stack):
    print(color("\n" + error_type + ":\n\t" + message + "\n\nStack Trace:\n" +
                format_trace(call_stack.get_stack()), fg="red"))
    sys.exit(1)

def format_trace(call_stack):
    trace = ""
    for line in call_stack:
        if "\n" not in line.line:
            line.line += "\n"
        trace += "\t" + line.get_line_info()
    return trace