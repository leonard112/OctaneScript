from colors import color
import sys


def fail(message, error_type, call_stack):
    print(color("\n" + error_type + ":\n\t" + message + "\n\nStack Trace:\n" +
                format_trace(call_stack.get_stack()), fg="red"))
    sys.exit(1)

def format_trace(call_stack):
    trace = ""
    for line in call_stack:
        if (line.file_name == "REPL"):
            line.line_number += 1
        trace += "\t" + line.get_line_info()
    return trace