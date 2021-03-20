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
    max_length = 40
    count = 0
    for line in call_stack:
        if count == max_length:
            trace += "\t...\n"
            break
        if "\n" not in line.line:
            line.line += "\n"
        trace += "\t" + line.get_line_info()
        count += 1
    return trace