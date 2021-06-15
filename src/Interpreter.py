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
import io
from contextlib import redirect_stdout
import sys
import random
import time
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
        self.exit_repl_on_error = False
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
            line_raw = input("| " + str(self.repl_counter+1) + "   >> ") + "\n"
            self.lines.append(line_raw)
            line = Line(line_raw, self.repl_counter, "REPL")
            self.call_stack.push(line)
            try:
                self.execute(self.call_stack)
            except SystemExit as e:
                rc = int(str(e))
                if rc == 0 or self.exit_repl_on_error == True:
                    raise sys.exit(rc)
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
            if repeat_to == 0:
                fail("The number of times to repeat the code block cannot be '0'." , self.error_type, self.call_stack)
            if step == 0:
                fail("\"step\" cannot be '0'." , self.error_type, self.call_stack)
            if repeat_to - start > 0 and step < 0:
                fail("\"step\" cannot be less than '0' if the difference between the amount of times to repeat the code block and \"start\" is greater than '0'." , self.error_type, self.call_stack)
            if repeat_to - start < 0 and step > 0:
                fail("\"step\" cannot be greater than '0' if the difference between the amount of times to repeat the code block and \"start\" is less than '0'." , self.error_type, self.call_stack)
            repeat_lines = self.get_nested_code(line_number + 1)
            for i in range(start, repeat_to, step):
                if is_counter == True:
                    self.variables[counter] = i
                if self.script_name == "REPL" and self.in_nested_repl == False:
                    self.in_nested_repl = True
                    repl_repeat_lines = repeat_lines[:-1]
                    self.repl_counter -= len(repl_repeat_lines)
                    self.run_script(repl_repeat_lines, None)
                    self.repl_counter += len(repl_repeat_lines)
                    self.in_nested_repl = False
                else:
                    self.run_script(repeat_lines, line_number + 1)
            if is_counter == True:
                self.variables.pop(counter)
            if counter_overrides_an_existing_variable == True:
                self.variables[counter] = counter_original_value
            return line_number + len(repeat_lines) + 1

        elif function == "while":
            parameters = ' '.join(parameters.split())
            if parameters == '':
                fail("'while' must take a boolean argument." , self.error_type, self.call_stack)
            boolean = self.resolve_function_calls(parameters, line_number)
            b = Boolean(boolean, call_stack, self.variables)
            while_lines = self.get_nested_code(line_number + 1)
            while b.evaluate() == True:
                if self.script_name == "REPL" and self.in_nested_repl == False:
                    self.in_nested_repl = True
                    repl_while_lines = while_lines[:-1]
                    self.repl_counter -= len(repl_while_lines)
                    self.run_script(repl_while_lines, None)
                    self.repl_counter += len(repl_while_lines)
                    self.in_nested_repl = False
                else:
                    self.run_script(while_lines, line_number + 1)
                boolean = self.resolve_function_calls(parameters, line_number)
                b = Boolean(boolean, call_stack, self.variables)
            return line_number + len(while_lines) + 1

        if function == "for":
            parameters = ' '.join(parameters.split())
            parameter_tokens = parameters.split()
            if len(parameter_tokens) < 3:
                fail("'for' requires at least 3 arguments. Correct syntax for 'repeat for': 'repeat for element in array'" , self.error_type, self.call_stack)
            if parameter_tokens[1] != "in":
                fail("'for' requires the 'in' keyword. Correct syntax for 'repeat for': 'repeat for element in array'" , self.error_type, self.call_stack)
            element_variable = parameter_tokens[0]
            element_variable_overrides_existing_variable = False
            element_variable_original_value = None
            if element_variable in self.variables:
                element_variable_overrides_existing_variable = True
                element_variable_original_value = self.variables[element_variable]
            array_expression = self.resolve_function_calls(' '.join(parameter_tokens[2:]), line_number)
            e = Expression(array_expression, self.call_stack, self.variables)
            array = e.evaluate()
            if type(array) != list:
                fail(f"'for' can only iterate over an array. '{parameter_tokens[2:]}' is not an array." , self.error_type, self.call_stack)
            for_lines = self.get_nested_code(line_number + 1)
            for element in array:
                self.variables[element_variable] = element
                if self.script_name == "REPL" and self.in_nested_repl == False:
                    self.in_nested_repl = True
                    repl_for_line = for_lines[:-1]
                    self.repl_counter -= len(repl_for_line)
                    self.run_script(repl_for_line, None)
                    self.repl_counter += len(repl_for_line)
                    self.in_nested_repl = False
                else: 
                    self.run_script(for_lines, line_number + 1)
            if element_variable_overrides_existing_variable == True:
                self.variables[element_variable] = element_variable_original_value
            return line_number + len(for_lines) + 1

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
            f = Function(parameters, function_body, self.call_stack, self.functions, self.variables, function_start)
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
            if self.script_name == "REPL" and self.exit_repl_on_error == False:
                output = io.StringIO()
                with redirect_stdout(output):
                    p.print()
                output = output.getvalue()
                print("\t " + output[:-1].replace("\n", "\n         "))
            else:
                p.print()
            return line_number

        elif function[:3] == "log":
            parameters = self.resolve_function_calls(parameters, line_number)
            l = Logger(function, parameters, call_stack, self.variables)
            if self.script_name == "REPL":
                output = io.StringIO()
                with redirect_stdout(output):
                    l.log()
                output = output.getvalue()
                print("\t " + output[:-1].replace("\n", "\n         "))
            else:
                l.log()
            return line_number

        elif function == "set":
            parameters = self.resolve_function_calls(parameters, line_number)
            parameter_tokens = parameters.split()
            if parameter_tokens[-1] == "input":
                user_input = input("")
                parameters = ' '.join(parameter_tokens[:-1]) + ' "' + user_input + '"'
            elif parameter_tokens[2] == "input":
                prompt = ' '.join(parameter_tokens[3:])
                expression = Expression(prompt, self.call_stack, self.variables)
                prompt = expression.evaluate()
                user_input = input(prompt)
                parameters = ' '.join(parameter_tokens[:2]) + ' "' + user_input + '"'
            elif parameter_tokens[2] == "randomInteger":
                random_integer_parameters = ' '.join(parameter_tokens[3:])
                random_integer_parameter_tokens = random_integer_parameters.split(",")
                random_integer_parameter_tokens_length = len(random_integer_parameter_tokens)
                if random_integer_parameter_tokens_length > 2 or random_integer_parameter_tokens_length < 1:
                    fail("'randomInteger' can only take 2 parameters, and must take at least 1.", self.error_type, call_stack)
                if random_integer_parameter_tokens_length == 2:
                    expression = Expression(random_integer_parameter_tokens[0], self.call_stack, self.variables)
                    lower_limit = expression.evaluate()
                    expression = Expression(random_integer_parameter_tokens[1], self.call_stack, self.variables)
                    upper_limit = expression.evaluate()
                if random_integer_parameter_tokens_length == 1:
                    lower_limit = 0
                    expression = Expression(random_integer_parameter_tokens[0], self.call_stack, self.variables)
                    upper_limit = expression.evaluate()
                if type(lower_limit) != int or type(upper_limit) != int:
                    fail("'randomInteger' can only take integer parameters.", self.error_type, call_stack)
                if upper_limit < lower_limit:
                    fail("Lower limit cannot be greater than upper limit.", self.error_type, call_stack)
                parameter_tokens[2] = str(random.randint(lower_limit, upper_limit))
                parameters = ' '.join(parameter_tokens[:3])
            elif parameter_tokens[-1] == "randomDecimal":
                parameter_tokens[-1] = str(random.random())
                parameters = ' '.join(parameter_tokens)
            setter = Setter(parameters, call_stack, self.variables, self.functions)
            self.variables.update(setter.set())
            return line_number

        elif function == "append" or function == "prepend" or function == "push":
            parameters = self.resolve_function_calls(parameters, line_number)
            parameter_tokens = parameters.split()
            if parameter_tokens[-2] != "to":
                fail(f"'{function}' operation missing 'to' keyword." , self.error_type, call_stack)
            expression = Expression(' '.join(parameter_tokens[:-2]), self.call_stack, self.variables)
            value = expression.evaluate()
            array = parameter_tokens[-1]
            if array not in self.variables:
                fail(f"The array '{array}' does not exist in the current scope.", self.error_type, call_stack)
            if type(self.variables[array]) != list:
                fail("Values can only be appended to arrays.", self.error_type, call_stack)
            if function == "append":
                self.variables[array].append(value)
            elif function == "prepend" or function == "push" :
                self.variables[array].insert(0, value)
            return line_number

        elif function == "pop" or function == "removeFirst" or function == "removeLast" or function == "remove":
            parameters = self.resolve_function_calls(parameters, line_number)
            parameters = " " + parameters
            if " from " not in parameters:
                fail(f"'{function}' operation missing 'from' keyword.", self.error_type, call_stack)
            required_tokens = 2
            parameter_tokens = parameters.split(" from ")
            if " into " in parameters:
                required_tokens = 3
                parameter_tokens = parameter_tokens[:-1] + parameter_tokens[-1].split(" into ")
                variable = parameter_tokens[-1]
            if len(parameter_tokens) != required_tokens:
                fail(f"The '{function}' function must contain one instance of the 'from' keyword and may contain one instance of the 'into' keyword.", self.error_type, call_stack)
            array = parameter_tokens[1].strip()
            if array not in self.variables:
                fail(f"The array '{array}' does not exist in the current scope.", self.error_type, call_stack)
            if type(self.variables[array]) != list:
                fail(f"Elements may only be removed from arrays.", self.error_type, call_stack)
            if len(self.variables[array]) == 0:
                fail(f"Elements cannot be removed from array '{array}' because it is empty.", self.error_type, call_stack)
            if function != "remove" and parameter_tokens[0].strip() != '':
                fail(f"The '{function}' function was given too many arguments.", self.error_type, call_stack)
            if function == "pop" or function == "removeFirst":
                removed_value = self.variables[array][0]
                self.variables[array] = self.variables[array][1:]
            elif function == "removeLast":
                removed_value = self.variables[array][-1]
                self.variables[array] = self.variables[array][:-1]
            elif function == "remove":
                index_expression = parameter_tokens[0]
                index = Expression(index_expression, self.call_stack, self.variables).evaluate()
                if type(index) != int:
                    fail(f"Array index '{index_expression}' is not an integer. Array index must be an integer.", self.error_type, call_stack)
                try:
                    removed_value = self.variables[array][index]
                    self.variables[array].pop(index)
                except:
                    fail(f"Array index '{index_expression}' is out of range for array '{array}'.", self.error_type, call_stack)
            if required_tokens == 3:
                setter = Setter(parameters, call_stack, self.variables, self.functions)
                if setter.is_variable_name_valid(variable) == True:
                    self.variables[variable] = removed_value
            return line_number

        elif function == "merge":
            parameters = self.resolve_function_calls(parameters, line_number)
            if " into " not in parameters:
                fail(f"'{function}' operation missing 'into' keyword.", self.error_type, call_stack)
            parameter_tokens = parameters.split(" into ")
            if len(parameter_tokens) != 2:
                fail(f"The '{function}' function may only contain one instance of the 'into' keyword.", self.error_type, call_stack)
            from_array = Expression(parameter_tokens[0].strip(), self.call_stack, self.variables).evaluate()
            into_array = parameter_tokens[-1].strip()
            if into_array not in self.variables:
                fail(f"The array '{into_array}' does not exist in the current scope.", self.error_type, call_stack)
            if type(from_array) != list:
                fail(f"Only arrays can be merged. {from_array} is not an array", self.error_type, call_stack)
            if type(self.variables[into_array]) != list:
                fail(f"Only arrays can be merged. {into_array} is not an array", self.error_type, call_stack)
            self.variables[into_array] = self.variables[into_array] + from_array
            return line_number

        elif function == "sort" or function == "sortReverse":
            if parameters not in self.variables:
                fail(f"Array to sort must be stored in a variable. '{parameters}' is not a variable", self.error_type, call_stack)
            if type(self.variables[parameters]) != list:
                fail(f"Only arrays can be sorted. '{parameters}'' is not an array", self.error_type, call_stack)
            if function == "sort":
                self.variables[parameters].sort()
            else:
                self.variables[parameters].sort(reverse=True)
            return line_number

        elif function == "sleep":
            parameters = self.resolve_function_calls(parameters, line_number)
            seconds = Expression(parameters, self.call_stack, self.variables).evaluate()
            if type(seconds) == int or type(seconds) == float:
                time.sleep(seconds)
            else:
                fail("Number of seconds to sleep for must be a number.", self.error_type, call_stack)
            return line_number

        elif function == "exit":
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
        self.call_stack.pop()
        if self.recursion_depth == 0:
            self.variables = self.variables_out_of_scope


    def resolve_function_calls(self, parameters, line_number):
        if len(parameters) == 0:
            return parameters
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
                    token = token.strip("<").strip(">")
                    if token[0] == "(" or token[0] == "[":
                        specialized_expression_functions = self.get_functions_from_specialized_expression(token, function)
                        for specialized_token in specialized_expression_functions:
                            function_calls += [specialized_token]
                    else:
                        token = token.strip(",")
                        function_calls += [token]
        return function_calls

    def get_functions_from_specialized_expression(self, expression, function):
        parameter_tokens = expression.split(function)
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
        parameter_tokens = expression.split(f" {function}")
        for token in parameter_tokens:
            token = token.strip().strip("(").strip("[")
            if token[-4:] == "type":
                functions += function
        return functions

    
    def execute_functions(self, function_calls, parameter_tokens, line_number):
        parameter_tokens_length = len(parameter_tokens)
        for i in range(0, parameter_tokens_length, 1):
            for function_call in function_calls:
                if parameter_tokens[i][0] == '"' and parameter_tokens[i][-1] == '"':
                    pass
                elif function_call.split("(")[0] not in self.functions:
                    pass
                elif function_call in parameter_tokens[i] and "(" not in function_call and "type" in parameter_tokens[i]:
                    parameter_tokens[i] = ' '.join(parameter_tokens[i].split())
                    parameter_tokens[i] = parameter_tokens[i].replace(f"type {function_call}", "@Type:Function")
                elif function_call in parameter_tokens[i] and parameter_tokens[i-1] != "type":
                    function_name = function_call.split("(")[0]
                    self.execute_function(function_call, "", function_name, line_number)
                    return_value = self.functions[function_name].return_value
                    if type(return_value) == list:
                        p = Printer("print", "", self.call_stack, self.variables)
                        return_value = p.stringify_array(return_value)
                    e = Expression("", self.call_stack, self.variables)
                    if e.is_value_type(return_value):
                        return_value = e.create_string_representation_of_type(return_value)
                    return_value = str(return_value)
                    if return_value == "True" or return_value == "False":
                        return_value = return_value.lower()
                    parameter_tokens[i] = parameter_tokens[i].replace(function_call, return_value)
                elif function_call in parameter_tokens[i] and parameter_tokens[i-1] == "type":
                    i -= 1
                    parameter_tokens.pop(i)
                    parameter_tokens[i] = "@Type:Function"

        return parameter_tokens


    def execute_function(self, function, parameters, function_name, line_number):
        function_name_length = len(function_name)
        if function_name_length == len(function):
            fail(f"'{function}' is an incomplete function call. Function call systax: 'myFunction(param1, param2)'" , self.error_type, self.call_stack)
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
                line_raw = input("| " + str(self.repl_counter+1) + "    ~ ") + "\n"
                if line_raw.strip()[:2] == "if":
                    required_end_count += 1
                elif line_raw.strip()[:3] == "for":
                    required_end_count += 1
                elif line_raw.strip()[:5] == "while":
                    required_end_count += 1
                elif line_raw.strip()[:6] == "repeat":
                    required_end_count += 1
                elif line_raw.strip() == "end":
                    end_count += 1
                elif line_raw.strip()[:8] == "function":
                    line = Line(line_raw, self.repl_counter, "REPL")
                    self.call_stack.push(line)
                    fail("A function cannot be defined inside a nestable." , self.error_type, self.call_stack)
                if required_end_count == end_count:
                    nestable_lines.append(line_raw)
                    return nestable_lines
                nestable_lines.append(line_raw)

        line_count = len(self.lines)
        for i in range(start_line,line_count,1):
            line_raw = self.lines[i]
            if line_raw.strip()[:2] == "if":
                required_end_count += 1
            elif line_raw.strip()[:3] == "for":
                required_end_count += 1
            elif line_raw.strip()[:5] == "while":
                required_end_count += 1
            elif line_raw.strip()[:6] == "repeat":
                required_end_count += 1
            elif line_raw.strip() == "end":
                end_count += 1
            elif line_raw.strip()[:8] == "function":
                line = Line(line_raw, i + self.repl_counter, self.script_name)
                self.call_stack.push(line)
                fail("A function cannot be defined inside a nestable." , self.error_type, self.call_stack)
            if required_end_count == end_count:
                return nestable_lines
            nestable_lines.append(line_raw)
        fail("Missing end to nestable.", self.error_type, self.call_stack)