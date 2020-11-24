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


class Interpreter:
    def __init__ (self, script_name):
        self.script_name = script_name
        self.lines = []
        self.variables = {}
        self.call_stack = Stack()
        self.repl_counter = 0
        self.in_if_chain = False
        self.looking_for_else = False
        self.in_nested_repl = False
        self.error_type = "Interpreter Error"
        

    def run(self):
        if self.script_name != "REPL":
            self.script_name = os.path.abspath(self.script_name)

            try:
                script = open(self.script_name, "r")
            except:
                print(color("File \"" + self.script_name + "\" not found.", fg="red"))
                sys.exit()

            self.lines = script.readlines()
            self.run_script(self.lines, 0)
            
        else:
            self.repl_counter = 1
            try:
                self.run_repl()
            except SystemExit as e:
                rc = int(str(e))
                if rc == 0:
                    return
                raise sys.exit(rc)

    
    def run_script(self, lines, overall_script_position):
        if overall_script_position == None:
            self.lines = lines
            overall_script_position = 0

        line_count = len(lines)
        i = 0

        while(i < line_count) :
            line = Line(lines[i].lstrip(), i + overall_script_position + self.repl_counter, self.script_name)
            self.call_stack.push(line)
            i = self.execute(self.call_stack) - overall_script_position
            self.call_stack.pop()
            i += 1


    def run_repl(self):
        line = ""

        while True:
            line_raw = input(">> ") + "\n"
            self.lines.append(line_raw)
            line = Line(line_raw, self.repl_counter, "REPL")
            self.call_stack.push(line)
            self.execute(self.call_stack)
            if self.call_stack.peek() != None:
                self.call_stack.pop()
            self.repl_counter += 1


    def find_else(self, lines, line_number):
        line_count = len(lines)
        for i in range(1, line_count, 1):
            line_raw = lines[i]
            if line_raw.strip() == "else" or line_raw.strip()[:6] == "elseIf":
                self.looking_for_else = True
                return line_number + i
        return line_number + line_count


    def execute(self, call_stack):
        line_raw = call_stack.peek().line
        function = line_raw.split(' ')[0].strip()
        parameters = line_raw[len(function)+1:].strip()
        line_number = call_stack.peek().line_number - self.repl_counter

        if function == "#" or function == "":
            print(end="")
            return line_number

        elif function == "if" or function == "elseIf" or function == "else":
            if function == "elseIf" or function == "else":
                if self.in_if_chain == False:
                    fail("Dangling \"" + function + "\".", self.error_type, call_stack)
                elif self.looking_for_else == False:
                    return line_number + len(self.get_conditional_code(line_number + 1))
            bool_result = False
            if function == "if" or function == "elseIf":
                self.in_if_chain = True
                self.looking_for_else = False
                b = Boolean(parameters, call_stack, self.variables)
                bool_result = b.evaluate()
            conditional_lines = self.get_conditional_code(line_number + 1)
            if self.script_name == "REPL" and self.in_nested_repl == False:
                self.in_nested_repl = True
                self.call_stack.pop()
                self.repl_counter -= 1
                self.run_script([line_raw] + conditional_lines, None)
                self.in_nested_repl = False
                self.repl_counter += len(conditional_lines)
                return
            if bool_result == True or function == "else":
                self.run_script(conditional_lines, line_number + 1)
                self.in_if_chain = True
                line_number += len(conditional_lines)
            else:
                line_number = self.find_else(conditional_lines, line_number)
            return line_number

        elif function[:3] == "end":
            if (self.in_if_chain == False):
                fail("Extra or dangling \"end\".", self.error_type, self.call_stack)
            self.in_if_chain = False
            return line_number

        elif function[:5] == "print":
            p = Printer(function, parameters, call_stack, self.variables)
            p.print()
            return line_number

        elif function[:3] == "log":
            l = Logger(function, parameters, call_stack, self.variables)
            l.log()
            return line_number

        elif function[:3] == "set" and len(function) == 3:
            setter = Setter(parameters, call_stack, self.variables)
            self.variables.update(setter.set())
            return line_number

        elif function[:4] == "exit" and len(function) == 4:
            sys.exit(0)
        else:
            fail("Unknown function.", self.error_type, call_stack)

    def get_conditional_code(self, start_line):
        conditional_lines = []
        required_end_count = 1
        end_count = 0

        if self.script_name == "REPL" and self.in_nested_repl == False:
            while(True):
                line_raw = input(" ~ ") + "\n"
                if line_raw.strip()[:2] == "if":
                    required_end_count += 1
                elif line_raw.strip() == "end":
                    end_count += 1
                if required_end_count == end_count:
                    conditional_lines.append(line_raw)
                    return conditional_lines
                conditional_lines.append(line_raw)

        line_count = len(self.lines)
        for i in range(start_line,line_count,1):
            line_raw = self.lines[i]
            if line_raw.strip()[:2] == "if":
                required_end_count += 1
            elif line_raw.strip() == "end":
                end_count += 1
            if required_end_count == end_count:
                return conditional_lines
            conditional_lines.append(line_raw)
        fail("Missing end to conditional.", self.error_type, self.call_stack)




        
