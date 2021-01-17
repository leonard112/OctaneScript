# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from core.Fail import fail
from core.Expression import Expression
from core.Setter import Setter


class Function:
    def __init__ (self, function_definition, call_stack, function_start):
        self.call_stack = call_stack
        self.function_variables = {}
        self.function_variable_count = 0
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
                self.function_variables = self.get_function_variables(parameters)
                self.function_variable_count = len(self.function_variables)
            else:
                raise Exception
        except Exception:
            fail("Bad function definition.", self.error_type, self.call_stack)

    
    def get_function_variables(self, parameters):
        parameters = self.tokenize_parameters(parameters)
        function_variables = {}
        for parameter in parameters:
            parameter = parameter.strip()
            setter = Setter("", "", "")
            if setter.is_variable_name_valid(parameter) == False:
                raise Exception
            function_variables[parameter] = None
        return function_variables


    def populate_variables(self, parameters):
        try:
            parameters = self.tokenize_parameters(parameters)
            if self.function_variable_count != len(parameters):
                raise Exception
            for variable in self.function_variables:
                expression = Expression(parameters[0], self.call_stack, self.function_variables)
                self.function_variables[variable] = expression.evaluate()
                parameters.pop(0)
        except Exception:
            fail("Bad parameter subsitution.", self.error_type, self.call_stack)


    def tokenize_parameters(self, parameters):
        if parameters[0] != "(" or parameters [-1] != ")":
            raise Exception
        parameters = parameters[1:-1]
        if parameters[0] == "," or parameters[-1] == ",":
            raise Exception
        return parameters.split(",")