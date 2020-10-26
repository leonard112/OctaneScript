from core.Math import Math
from core.Fail import fail

class Expression:
    def __init__ (self, expression, line, variables):
        self.expression = expression
        self.line = line
        self.variables = variables
        self.error_type = "Expression Error"

        self.i = 0
        self.end_index = 0
        self.requires_dot = -1
        self.valid_start = 0
        self.result = ""

    def evaluate (self):
        while self.i < len(self.expression):
            if self.i == self.valid_start:
                if self.expression[self.i] == '"' or self.expression[self.i] == "'":
                    self.evaluate_string()
                elif self.expression[self.i] == '(':
                    self.evaluate_math()
                else:
                    try:
                        self.resolve_number()
                    except:
                        self.resolve_variable()
            elif self.i == self.requires_dot:
                if self.expression[self.i] != ".":
                    fail("Missing '.' operator for string concatenation.", self.error_type, self.line)
                elif self.i == len(self.expression) - 1:
                    fail("Extra '.' operator at end of line.", self.error_type, self.line)
            self.i += 1

        return self.result

    def evaluate_string(self):
        quote_type = ""
        if self.expression[self.i] == '"':
            quote_type = '"'
        else:
            quote_type = "'"

        self.end_index = self.get_next_occurance(self.i+1, quote_type)
        self.result += self.expression[self.i+1:self.end_index]
        self.set_i_to_end_index_and_update_valid_start_and_requries_dot()

    def resolve_number(self):
        self.result += str(float(self.expression[self.i:].split(' ', 1)[0]))
        self.i += len(self.expression[self.i:].split(' ', 1)[0])-1
        self.update_valid_start_and_requires_dot()

    def evaluate_math(self):
        self.end_index = self.get_last_occurance(self.i+1, self.expression[self.i:],  ')')
        math_expression = Math(self.expression[self.i+1:self.end_index], self.line, self.variables)
        self.result += str(math_expression.calculate())
        self.set_i_to_end_index_and_update_valid_start_and_requries_dot()

    def resolve_variable(self):
        self.result += self.get_variable(self.expression[self.i:].split(' ', 1)[0])
        self.i += len(self.expression[self.i:].split(' ', 1)[0])-1
        self.update_valid_start_and_requires_dot()

    def get_next_occurance(self, start_index, char):
        for i in range(start_index, len(self.expression), 1):
            if self.expression[i] == char:
                return i
        fail("Missing quote on string", self.error_type, self.line)

    def get_last_occurance(self, start_index, expression, char):
        for i in range(len(expression)-1, start_index, -1):
            if expression[i] == char:
                return i
        fail("Missing parentheses on Math expression", self.error_type, self.line)

    def set_i_to_end_index_and_update_valid_start_and_requries_dot(self):
        self.i = self.end_index
        self.update_valid_start_and_requires_dot()

    def update_valid_start_and_requires_dot(self):
        self.valid_start = self.i + 4
        self.requires_dot = self.i + 2

    def get_variable(self, variable):
        if variable in self.variables:
            return self.variables[variable]
        fail("Variable not found.", self.error_type, self.line)
                