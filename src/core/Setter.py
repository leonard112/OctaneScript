from core.Fail import fail
from core.Expression import Expression
from Reserved import reserved

class Setter:
    def __init__ (self, parameters, line, variables):
        self.parameters = parameters
        self.line = line
        self.variables = variables
        self.error_type = "Set Error"
    
    def set(self):
        variable = self.get_variable_name()
        value = self.get_value(self.parameters[len(variable):])
        return {variable : value}

    def get_variable_name(self):
        for i in range(0, len(self.parameters), 1):
            if self.parameters[i] == " ":
                if self.is_variable_valid(self.parameters[:i]):
                    return self.parameters[:i]
                fail("Bad variable name.", self.error_type, self.line)

    def get_value(self, parameters):
        if parameters[0:4] == " to ":
            expression = Expression(parameters[4:], self.line, self.variables)
            return expression.evaluate()
        fail("Bad syntax.", self.error_type, self.line)

    def is_variable_valid(self, variable):
        valid_characters = "abcdefghijklmnopqrstuvwxyz"
        valid_character_count = 0

        for char in variable:
            for valid_char in valid_characters:
                if char.lower() == valid_char:
                    valid_character_count += 1

        for word in reserved:
            if word == variable:
                return False

        if valid_character_count == len(variable):
            return True
        return False
        