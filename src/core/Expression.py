from core.Fail import fail

class Expression:
    def __init__ (self, expression, line, variables):
        self.expression = expression
        self.line = line
        self.variables = variables
        self.error_type = "Expression Error"

    def evaluate (self):

        result = ""
        i = 0
        valid_start = 0
        requires_dot = -1

        while i < len(self.expression):
            if i == valid_start:
                if self.expression[i] == '"' or self.expression[i] == "'":
                    quote_type = ""
                    if self.expression[i] == '"':
                        quote_type = '"'
                    else:
                        quote_type = "'"

                    start_index = i+1
                    i = self.get_next_occurance(start_index, quote_type)
                    result += self.expression[start_index:i]
                    valid_start = i + 4
                    requires_dot = i + 2
                else:
                    result += self.get_variable(self.expression[i:].split(' ', 1)[0])
                    i += len(self.expression[i:].split(' ', 1)[0])-1
                    valid_start = i + 4
                    requires_dot = i + 2
            elif i == requires_dot:
                if self.expression[i] != ".":
                    fail("Missing '.' operator for string concatenation.", self.error_type, self.line)
                elif i == len(self.expression) - 1:
                    fail("Extra '.' operator at end of line.", self.error_type, self.line)
            i += 1

        return result

    def get_next_occurance(self, start_index, char):
        for i in range(start_index, len(self.expression), 1):
            if self.expression[i] == char:
                return i
        fail("Missing quote on string", self.error_type, self.line)

    def get_variable(self, variable):
        if variable in self.variables:
            return self.variables[variable]
        fail("Variable not found.", self.error_type, self.line)
                