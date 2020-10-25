from core.Printer import Printer
from core.Line import Line
from core.Setter import Setter
from core.Fail import fail
from colors import color
import os
import sys
from Reserved import reserved

variables = {}

class Interpreter:
    def __init__ (self, script_name):
        self.script_name = script_name

    def run(self):
        if self.script_name != "repl":
            self.script_name = os.path.abspath(self.script_name)

            try:
                script = open(self.script_name, "r")
            except:
                print(color("File \"" + self.script_name + "\" not found.", fg="red"))
                sys.exit()

            lines = script.readlines()
            line_count = len(lines)

            for i in range(0,line_count,1) :
                line = Line(lines[i].lstrip(), i, self.script_name)
                self.execute(line)
        else:
            line = ""
            while True:
                line = Line(input(">> "), None, "REPL")
                self.execute(line)

    def execute(self, line):
        function = line.get_line().split(' ')[0].strip()
        parameters = line.get_line()[len(function)+1:].strip()

        if function == "#" or function == "":
            print(end="")
        elif function[:5] == "print":
            p = Printer(function, parameters, line.get_line_info(), variables)
            p.print()
        elif function[:3] == "set" and len(function) == 3:
            setter = Setter(parameters, line.get_line_info(), variables)
            variables.update(setter.set())
        elif function[:4] == "exit" and len(function) == 4:
            sys.exit(0)
        else:
            fail("Unknown function.", "Interpreter Error", line.get_line_info())
