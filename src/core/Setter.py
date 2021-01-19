# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

# IMPORTANT: Real data type must be stored when setting a variable (i.e. store integer 1 NOT string "1")

from core.Fail import fail
from core.Expression import Expression
from Reserved import reserved

class Setter:
    def __init__ (self, parameters, call_stack, variables, functions):
        self.parameters = parameters
        self.call_stack = call_stack
        self.variables = variables
        self.functions = functions
        self.error_type = "Set Error"

    
    def set(self):
        variable = self.get_variable_name()
        value = self.get_value(self.parameters[len(variable):])
        if value == "true":
            value = True
        elif value == "false":
            value = False
        return {variable : value}


    def get_variable_name(self):
        for i in range(0, len(self.parameters), 1):
            if self.parameters[i] == " ":
                if self.is_variable_name_valid(self.parameters[:i]):
                    return self.parameters[:i]


    def get_value(self, parameters):
        if parameters[0:4] == " to ":
            expression = Expression(parameters[4:], self.call_stack, self.variables)
            return expression.evaluate()
        fail("Bad syntax.", self.error_type, self.call_stack)


    def is_variable_name_valid(self, variable):
        valid_characters = "abcdefghijklmnopqrstuvwxyz"
        valid_character_count = 0

        for char in variable:
            for valid_char in valid_characters:
                if char.lower() == valid_char:
                    valid_character_count += 1

        for word in reserved:
            if word == variable:
                fail("The name \"" + variable + "\" is a reserved word.", self.error_type, self.call_stack)

        for function in self.functions:
            if function == variable:
                fail("The name \"" + variable + "\" is already used to define a function.", self.error_type, self.call_stack)

        if valid_character_count == len(variable):
            return True
        fail("Variable names may only contain letters.", self.error_type, self.call_stack)
        