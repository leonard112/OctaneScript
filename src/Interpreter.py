from core.Printer import Printer
from core.Logger import Logger
from core.Line import Line
from core.Stack import Stack
from core.Setter import Setter
from core.Fail import fail
from core.Boolean import Boolean
from colors import color
import os
import sys
from Reserved import reserved


variables = {}
call_stack = Stack()


class Interpreter:
    def __init__ (self, script_name):
        self.script_name = script_name
        self.lines = None
        self.error_type = "Interpreter Error"
        

    def run(self):
        if self.script_name != "repl":
            self.script_name = os.path.abspath(self.script_name)

            try:
                script = open(self.script_name, "r")
            except:
                print(color("File \"" + self.script_name + "\" not found.", fg="red"))
                sys.exit()

            self.lines = script.readlines()
            self.run_script(self.lines, 0)
            
        else:
            self.run_repl()

    
    def run_script(self, lines, overall_script_position):
        line_count = len(lines)
        i = 0

        while(i < line_count) :
            line = Line(lines[i].lstrip(), i + overall_script_position, self.script_name)
            call_stack.push(line)
            i = self.execute(call_stack)
            call_stack.pop()
            i += 1


    def run_repl(self):
        line = ""

        while True:
            line = Line(input(">> "), None, "REPL")
            call_stack.push(line)
            self.execute(call_stack)
            call_stack.pop()


    def execute(self, call_stack):
        function = call_stack.peek().line.split(' ')[0].strip()
        parameters = call_stack.peek().line[len(function)+1:].strip()
        line_number = call_stack.peek().line_number

        if function == "#" or function == "":
            print(end="")
            return line_number

        elif function[:5] == "if" and len(function) == 2:
            b = Boolean(parameters, call_stack, variables)
            conditional_lines = self.get_conditional_code(line_number + 1)
            if b.evaluate() == True:
                self.run_script(conditional_lines, line_number + 1)
            line_number += len(conditional_lines) - 1
            return line_number

        elif function[:3] == "end":
            return line_number

        elif function[:5] == "print":
            p = Printer(function, parameters, call_stack, variables)
            p.print()
            return line_number

        elif function[:3] == "log":
            l = Logger(function, parameters, call_stack, variables)
            l.log()
            return line_number

        elif function[:3] == "set" and len(function) == 3:
            setter = Setter(parameters, call_stack, variables)
            variables.update(setter.set())
            return line_number

        elif function[:4] == "exit" and len(function) == 4:
            sys.exit(0)
        else:
            fail("Unknown function.", self.error_type, call_stack)

    def get_conditional_code(self, start_line):
        line_count = len(self.lines)
        conditional_lines = []
        required_end_count = 1
        end_count = 0

        for i in range(start_line,line_count,1):
            line_raw = self.lines[i]
            if line_raw.strip()[:2] == "if":
                required_end_count += 1
            if line_raw.strip() == "end":
                end_count += 1
            if required_end_count == end_count:
                return conditional_lines
            conditional_lines.append(line_raw)

        fail("Missing end to conditional.", self.error_type, call_stack)



        
