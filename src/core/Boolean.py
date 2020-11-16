from core.Fail import fail

class Boolean:
    def __init__ (self, expression, call_stack, variables):
        self.expression = expression
        self.call_stack = call_stack
        self.variables = variables
        self.error_type = "Boolean Error"

    def evaluate(self):
        if self.expression[0] != "[" and self.expression[-1] != "]":
            fail("Extra or missing parentheses.", self.error_type, self.call_stack)
        else:
            expression = self.expression[1:-1]
            if expression == "true":
                return True
            elif expression == "false":
                return False