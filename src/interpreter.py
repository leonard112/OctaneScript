from core.Printer import Printer
from core.Line import Line
from colors import color
import os
import sys

def run(script_name):
    if script_name != "repl":
        script_name = os.path.abspath(script_name)

        try:
            script = open(script_name, "r")
        except:
            print(color("File \"" + script_name + "\" not found.", fg="red"))
            sys.exit()

        lines = script.readlines()
        line_count = len(lines)

        for i in range(0,line_count,1) :
            line = Line(lines[i].lstrip(), i, script_name)
            execute(line)
    else:
        line = ""
        while True:
            line = Line(input(">> "), None, "REPL")
            execute(line)

def execute(line):
    function = line.get_line().split(' ')[0].strip()
    parameters = line.get_line()[len(function)+1:].strip()

    if function == "#" or function == "":
        print(end="")
    elif function[:5] == "print":
        p = Printer(function, parameters, line.get_line_info())
        p.print()
    elif function[:4] == "exit":
        sys.exit(0)