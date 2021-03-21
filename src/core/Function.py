# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull
from core.Fail import fail
from core.Expression import Expression
from core.Setter import Setter

# References for suppress_stdout_stderr
# https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
# https://creativecommons.org/licenses/by-sa/2.5/
@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


class Function:
    def __init__ (self, function_definition, function_body, call_stack, functions, global_variables, function_start):
        self.function_body = function_body
        self.call_stack = call_stack
        self.global_variables = global_variables
        self.functions = functions
        self.function_variables = {}
        self.function_variable_count = 0
        self.return_value = None
        self.error_type = "Function Error"
        try:
            if function_start < 0:
                raise Exception
            else:
                self.function_start = function_start

            self.function_name = function_definition.split("(")[0].rstrip()
            function_name_length = len(self.function_name)
            if function_definition[function_name_length] == "(":
                parameters = function_definition[function_name_length:]
                if len(parameters) > 2:
                    self.function_variables = self.get_function_variables(parameters)
                    self.function_variable_count = len(self.function_variables)
            else:
                fail("There cannot be spaces between the function name and \"(\" that begins the definition of the function parameters).", self.error_type, self.call_stack)
        except Exception:
            fail("Bad function definition.", self.error_type, self.call_stack)

    
    def get_function_variables(self, parameters):
        parameters = self.tokenize_parameters(parameters)
        function_variables = {}
        for parameter in parameters:
            parameter = parameter.strip()
            setter = Setter("", "", "", self.functions)
            if setter.is_variable_name_valid(parameter) == False:
                raise Exception
            function_variables[parameter] = None
        return function_variables


    def populate_variables(self, parameters):
        try:
            parameters = self.tokenize_parameters(parameters)
            if self.function_variable_count != len(parameters):
                fail("Too many or two few parameters.", self.error_type, self.call_stack)
            for variable in self.function_variables:
                try:
                    expression = Expression(parameters[0], self.call_stack, self.function_variables)
                    with suppress_stdout_stderr():
                        self.function_variables[variable] = expression.evaluate()
                except:
                    expression = Expression(parameters[0], self.call_stack, self.global_variables)
                    self.function_variables[variable] = expression.evaluate()
                parameters.pop(0)
        except Exception:
            fail("Bad parameter subsitution.", self.error_type, self.call_stack)


    def tokenize_parameters(self, parameters):
        if parameters[0] != "(" or parameters [-1] != ")":
            fail("Function parameters must be enclosed in parenthesis.", self.error_type, self.call_stack)
        parameters = parameters[1:-1]
        if len(parameters.replace(" ", "")) == 0:
            return []
        if parameters[0] == "," or parameters[-1] == ",":
            fail("Too many or two few comma delimiters.", self.error_type, self.call_stack)
        return parameters.split(",")
