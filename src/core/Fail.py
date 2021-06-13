# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from colors import color
from datetime import datetime
import traceback
import sys
import platform

error_report_banner = """========================================================================================
============================== OCTANESCRIPT ERROR REPORT ===============================
========================================================================================\n\n"""
octane_script_trace_banner = "\n__________________________________ OCTANESCRIPT TRACE __________________________________\n"
python_trace_banner = "\n_____________________________________ PYTHON TRACE _____________________________________\n"


def fail(message, error_type, call_stack):
    import Main
    metadata = """Time of Error: [%s]
OctaneScript Version: %s
OctaneScript Maintainer: %s
Python Version: %s
Architecture: %s
Processor: %s
Operating System: %s %s

If this error report was generated as a result of a bug with OctaneScript, you can submit
an issue at https://github.com/leonard112/OctaneScript/issues, and attach this error report.
""" % ('.'.join(str(datetime.now()).split('.')[:-1]), Main.version, Main.maintainer, platform.python_version(), platform.machine(), 
       platform.processor(), platform.system(), platform.version())
    error_summary = "\n" + error_type + ":\n\t" + message + "\n\nStack Trace:\n"
    console_trace = color(error_summary + format_trace(call_stack.get_stack(), False), fg="red")
    python_trace = python_trace_banner + "\n" + ''.join(traceback.format_list(traceback.extract_stack()))
    error_report_file_trace = error_report_banner + metadata + octane_script_trace_banner + error_summary + format_trace(call_stack.get_stack(), True) + python_trace
    error_report_file = open(".oserrorreport", "w")
    error_report_file.write(error_report_file_trace)
    print(console_trace, file=sys.stderr)
    sys.exit(1)

def format_trace(call_stack, is_log_file_trace):
    trace = ""
    max_length = 40
    count = 0
    for line in call_stack:
        if count == max_length and is_log_file_trace == False:
            trace += "\t...\n"
            break
        if "\n" not in line.line:
            line.line += "\n"
        trace += "\t" + line.get_line_info()
        count += 1
    return trace