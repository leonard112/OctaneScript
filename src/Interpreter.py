# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from core.Printer import Printer
from core.Expression import Expression
from core.Logger import Logger
from core.Line import Line
from core.Stack import Stack
from core.Setter import Setter
from core.Fail import fail
from core.Boolean import Boolean
from core.Function import Function
from colors import color
import os
import sys
from Reserved import reserved


class Interpreter:
    def __init__ (self, script_name):
        self.script_name = script_name
        self.lines = []
        self.variables = {}
        self.variables_out_of_scope = {}
        self.functions = {}
        self.recursion_depth = 0
        self.recursion_limit = 500
        self.call_stack = Stack()
        self.function_call_stack = Stack()
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
            try:
                self.run_repl()
            except SystemExit as e:
                rc = int(str(e))
                if rc == 0:
                    return
                raise sys.exit(rc)
            except KeyboardInterrupt:
                fail("Recieved Keyboard Interrupt (ctl+c). Terminating program..." , self.error_type, self.call_stack)

    
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
            if i < 0:
                return -1
            self.call_stack.pop()
            i += 1


    def run_repl(self):
        line = ""

        while True:
            line_raw = input("| " + str(self.repl_counter+1) + "\t\b\b>> ") + "\n"
            self.lines.append(line_raw)
            line = Line(line_raw, self.repl_counter, "REPL")
            self.call_stack.push(line)
            self.execute(self.call_stack)
            if self.call_stack.peek() != None:
                self.call_stack.pop()
            self.repl_counter += 1


    def find_else(self, lines, line_number):
        line_count = len(lines)
        i = 0
        while(i < line_count):
            line_raw = lines[i]
            if line_raw.strip()[:2] == "if":
                i = self.find_next_end(lines, line_count, i)
            elif line_raw.strip() == "else" or line_raw.strip()[:6] == "elseIf":
                self.looking_for_else = True
                return line_number + i
            i += 1
        return line_number + line_count


    def find_next_end(self, lines, line_count, start_line):
        for i in range(start_line, line_count, 1):
            if lines[i].strip()[:3] == "end":
                return i


    def execute(self, call_stack):
        line_raw = call_stack.peek().line
        function = line_raw.split(' ')[0].strip()
        parameters = line_raw[len(function)+1:].strip()
        line_number = call_stack.peek().line_number - self.repl_counter

        if function[:1] == "#" or function == "":
            print(end="")
            return line_number

        elif function == "if" or function == "elseIf" or function == "else":
            if self.recursion_depth > 0:
                self.in_nested_repl = True
            if function == "elseIf" or function == "else":
                if self.in_if_chain == False:
                    fail("Dangling \"" + function + "\".", self.error_type, call_stack)
                elif self.looking_for_else == False:
                    return line_number + len(self.get_nested_code(line_number + 1))
            bool_result = False
            if function == "if" or function == "elseIf":
                self.in_if_chain = True
                self.looking_for_else = False
                b = Boolean(parameters, call_stack, self.variables)
                bool_result = b.evaluate()
            conditional_lines = self.get_nested_code(line_number + 1)
            if self.script_name == "REPL" and self.in_nested_repl == False:
                self.in_nested_repl = True
                self.call_stack.pop()
                self.repl_counter -= len(conditional_lines)
                self.run_script([line_raw] + conditional_lines, None)
                self.repl_counter += len(conditional_lines)
                self.in_nested_repl = False
                return
            if bool_result == True or function == "else":
                exiting_function = self.run_script(conditional_lines, line_number + 1)
                if exiting_function == -1:
                    return -1
                self.in_if_chain = True
                line_number += len(conditional_lines)
            else:
                line_number = self.find_else(conditional_lines, line_number)
            return line_number

        elif function == "repeat":
            parameters = ' '.join(parameters.split())
            if parameters[:6] == "while ":
                boolean = self.resolve_function_calls(parameters[6:], line_number)
                b = Boolean(boolean, call_stack, self.variables)
                repeat_while_lines = self.get_nested_code(line_number + 1)
                if self.script_name == "REPL":
                    repeat_while_lines = repeat_while_lines[:-1]
                while b.evaluate() == True:
                    if self.script_name == "REPL":
                        self.repl_counter -= len(repeat_while_lines) + 1
                    self.run_script(repeat_while_lines, line_number + 1)
                    if self.script_name == "REPL":
                        self.repl_counter += len(repeat_while_lines) + 1
                    boolean = self.resolve_function_calls(parameters[6:], line_number)
                    b = Boolean(boolean, call_stack, self.variables)
                if self.script_name != "REPL": 
                    line_number += 1
                return line_number + len(repeat_while_lines)
            is_counter = False
            counter = None
            counter_overrides_an_existing_variable = False
            counter_original_value = None
            is_custom_step = False
            step = 1
            is_custom_start = False
            start = 0
            parameter_tokens = parameters.split(",")
            if len(parameter_tokens) > 1:
                option_tokens = parameter_tokens[1:]
                for option_token in option_tokens:
                    option_token = option_token.strip()
                    if option_token[:8] == "counter ":
                        if is_counter == True:
                            fail("\"counter\" already defined. Only define a counter once." , self.error_type, self.call_stack)
                        counter = option_token[8:]
                        if counter in self.variables:
                            counter_overrides_an_existing_variable = True
                            counter_original_value = self.variables[counter]
                        setter = Setter(counter + " to  0", call_stack, self.variables, self.functions)
                        self.variables.update(setter.set())
                        is_counter = True
                    elif option_token[:5] == "step ":
                        if is_custom_step == True:
                            fail("\"step\" already defined. Only define a step once." , self.error_type, self.call_stack)
                        step = self.resolve_function_calls(option_token[5:], line_number)
                        step_expression = Expression(step, self.call_stack, self.variables)
                        step = step_expression.evaluate()
                        if type(step) != int:
                                fail("\"step\" must be an integer." , self.error_type, self.call_stack)
                        is_custom_step = True
                    elif option_token[:6] == "start ":
                        if is_custom_start == True:
                            fail("\"start\" already defined. Only define a start value once." , self.error_type, self.call_stack)
                        start = self.resolve_function_calls(option_token[6:], line_number)
                        start_expression = Expression(start, self.call_stack, self.variables)
                        start = start_expression.evaluate()
                        if type(start) != int:
                                fail("\"start\" must be an integer." , self.error_type, self.call_stack)
                        is_custom_start = True
                    else:
                        fail("Unknown option for repeat loop." , self.error_type, self.call_stack)
            repeat_to = self.resolve_function_calls(parameter_tokens[0], line_number)
            repeat_expression = Expression(repeat_to, self.call_stack, self.variables)
            repeat_to = repeat_expression.evaluate()
            if type(repeat_to) != int:
                fail("The number of times to repeat the code block must be an integer." , self.error_type, self.call_stack)
            repeat_lines = self.get_nested_code(line_number + 1)
            if self.script_name == "REPL":
                repeat_lines = repeat_lines[:-1]
            for i in range(start, repeat_to, step):
                if is_counter == True:
                    self.variables[counter] = i
                if self.script_name == "REPL":
                        self.repl_counter -= len(repeat_lines) + 1
                self.run_script(repeat_lines, line_number + 1)
                if self.script_name == "REPL":
                        self.repl_counter += len(repeat_lines) + 1
            if is_counter == True:
                self.variables.pop(counter)
            line_number += len(repeat_lines)
            if self.script_name != "REPL": 
                line_number += 1
            if counter_overrides_an_existing_variable == True:
                self.variables[counter] = counter_original_value
            return line_number

        elif function == "function":
            function_name = parameters.split("(")[0].strip()
            if function_name in self.functions:
                fail("Function \"" + function_name + "\" is already defined." , self.error_type, self.call_stack)
            if function_name in self.variables:
                fail("Function cannot have the same name as a defined variable." , self.error_type, self.call_stack)
            function_start = line_number
            if self.script_name == "REPL":
                function_start = self.repl_counter
            function_body = self.get_nested_code(line_number + 1)
            function_end = len(function_body)
            f = Function(parameters, function_body, call_stack, self.functions, self.variables, function_start)
            self.functions[f.function_name] = f
            return line_number + function_end + 1

        elif function == "return":
            if self.recursion_depth == 0:
                fail("\"return\" can only be used in functions", self.error_type, self.call_stack)
            function_name = self.function_call_stack.peek()
            parameters = self.resolve_function_calls(parameters, line_number)
            e = Expression(parameters, self.call_stack, self.variables)
            return_value = e.evaluate()
            if type(return_value) == str:
                return_value = '"' + return_value + '"'
            self.functions[function_name].return_value = return_value
            self.function_cleanup()
            return -1

        elif function == "end":
            if self.in_if_chain == True:
                self.in_if_chain = False
                return line_number
            if self.recursion_depth > 0:
                self.function_cleanup()
                return line_number
            fail("Extra or dangling \"end\".", self.error_type, self.call_stack)

        elif function[:5] == "print":
            parameters = self.resolve_function_calls(parameters, line_number)
            p = Printer(function, parameters, call_stack, self.variables)
            p.print()
            return line_number

        elif function[:3] == "log":
            parameters = self.resolve_function_calls(parameters, line_number)
            l = Logger(function, parameters, call_stack, self.variables)
            l.log()
            return line_number

        elif function == "set" and len(function) == 3:
            parameters = self.resolve_function_calls(parameters, line_number)
            setter = Setter(parameters, call_stack, self.variables, self.functions)
            self.variables.update(setter.set())
            return line_number

        elif function == "exit" and len(function) == 4:
            sys.exit(0)
        else:
            try:
                function_name = function.split("(")[0]
                if function_name in self.functions:
                    self.execute_function(function, parameters, function_name, line_number)
                    return line_number
                else:
                    raise Exception
            except Exception:
                fail("Unknown function.", self.error_type, call_stack)


    def function_cleanup(self):
        self.recursion_depth -= 1
        if self.recursion_depth == 0:
            self.variables = self.variables_out_of_scope


    def resolve_function_calls(self, parameters, line_number):
        expression = Expression(parameters, self.call_stack, self.variables)
        parameter_tokens = expression.parse_expression(parameters, [])
        function_calls = self.get_functions(parameter_tokens)
        parameter_tokens = self.execute_functions(function_calls, parameter_tokens, line_number)
        return ' '.join(parameter_tokens)

    def get_functions(self, parameter_tokens):
        function_calls = []
        for token in parameter_tokens:
            for function in self.functions:
                if function in token:
                    if token.count('"') == 0 and token.count("'") == 0:
                        if token[0] == "(" or token[0] == "[":
                            specialized_expression_functions = self.get_functions_from_specialized_expression(token, function)
                            for specialized_token in specialized_expression_functions:
                                function_calls += [specialized_token]
                        else:
                            function_calls += [token]
        return function_calls

    def get_functions_from_specialized_expression(self, math_expression, function):
        parameter_tokens = math_expression.split(function)
        functions = []
        for token in parameter_tokens:
            if token.count("(") <= token.count(")") and token.count("(") >= 1:
                left_count = 0
                right_count = 0
                function_parameter = ""
                for char in token:
                    if char == "(":
                        left_count += 1
                    if char == ")":
                        right_count += 1
                    function_parameter += char
                    if right_count == left_count:
                        break 
                if function_parameter[0] == "(":
                    functions += [function + function_parameter]
        return functions

    
    def execute_functions(self, function_calls, parameter_tokens, line_number):
        parameter_tokens_length = len(parameter_tokens)
        for i in range(0, parameter_tokens_length, 1):
            for function_call in function_calls:
                if function_call in parameter_tokens[i]:
                    if parameter_tokens[i].count('"') == 0 and parameter_tokens[i].count("'") == 0:
                        function_name = function_call.split("(")[0]
                        self.execute_function(function_call, "", function_name, line_number)
                        return_value = self.functions[function_name].return_value
                        return_value = str(return_value)
                        if return_value == "True" or return_value == "False":
                            return_value =return_value.lower()
                        parameter_tokens[i] = parameter_tokens[i].replace(function_call, return_value)
        return parameter_tokens


    def execute_function(self, function, parameters, function_name, line_number):
        function_name_length = len(function_name)
        if function[function_name_length] == "(":
            function_parameters = function[function_name_length:] + parameters
            self.functions[function_name].populate_variables(function_parameters)
            if self.recursion_depth == 0:
                self.variables_out_of_scope = self.variables
            self.variables = self.functions[function_name].function_variables
            self.recursion_depth += 1
            if self.recursion_depth == self.recursion_limit:
                fail("Maximum recursion depth exceeded." , self.error_type, self.call_stack)
            self.function_call_stack.push(function_name)
            start_line = self.functions[function_name].function_start + 1
            function_body = self.functions[function_name].function_body
            function_call_line = self.repl_counter
            in_if_chain_tmp = self.in_if_chain
            looking_for_else_tmp = self.looking_for_else
            in_nested_repl_tmp = self.in_nested_repl
            self.in_if_chain = False
            self.looking_for_else = False
            self.in_nested_repl = False
            if self.script_name == "REPL":
                self.repl_counter = start_line
                self.run_script(function_body, None)
            else:
                self.run_script(function_body, start_line)
            self.in_if_chain = in_if_chain_tmp
            self.looking_for_else = looking_for_else_tmp
            self.in_nested_repl = in_nested_repl_tmp
            if self.script_name == "REPL":
                self.repl_counter = line_number
            self.repl_counter = function_call_line


    def get_nested_code(self, start_line):
        nestable_lines = []
        required_end_count = 1
        end_count = 0

        if self.script_name == "REPL" and self.in_nested_repl == False:
            while(True):
                self.repl_counter += 1
                line_raw = input("| " + str(self.repl_counter+1) + "\t\b\b~ ") + "\n"
                if line_raw.strip()[:2] == "if":
                    required_end_count += 1
                elif line_raw.strip() == "end":
                    end_count += 1
                elif line_raw.strip()[:8] == "function":
                    fail("A function cannot be defined inside a function or a conditional." , self.error_type, self.call_stack)
                if required_end_count == end_count:
                    nestable_lines.append(line_raw)
                    return nestable_lines
                nestable_lines.append(line_raw)

        line_count = len(self.lines)
        for i in range(start_line,line_count,1):
            line_raw = self.lines[i]
            if line_raw.strip()[:2] == "if":
                required_end_count += 1
            elif line_raw.strip() == "end":
                end_count += 1
            elif line_raw.strip()[:8] == "function":
                fail("A function cannot be defined inside a function or a conditional." , self.error_type, self.call_stack)
            if required_end_count == end_count:
                return nestable_lines
            nestable_lines.append(line_raw)
        fail("Missing end to nestable.", self.error_type, self.call_stack)




        
