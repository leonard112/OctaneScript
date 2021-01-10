import core.Expression
from core.NestableExpression import NestableExpression
from core.Fail import fail

class Boolean(NestableExpression):
    def __init__ (self, expression, call_stack, variables):
        self.expression = expression
        self.call_stack = call_stack
        self.variables = variables
        self.right_enclosing_symbol = "]"
        self.left_enclosing_symbol = "["
        self.error_type = "Boolean Error"
        self.symbols = ["lessThanEquals", "greaterThanEquals", "lessThan", "greaterThan", 
                        "equals", "notEquals", "and", "or", "[", "]", "true", "false"]

    def evaluate(self):
        if self.expression[0] != "[" or self.expression[-1] != "]":
            fail("Extra or missing brackets.", self.error_type, self.call_stack)
        result = self.evaluate_nestable_expression(self.parse_expression(self.expression, []), 
                                                 self.perform_operation)[0].lower()
        if result == "false":
            return False
        else:
            return True
    
    def perform_operation(self, tokens):
        return {
            'equals' : self.resolve(tokens[0]) == self.resolve(tokens[2]),
            'lessThan' : self.resolve(tokens[0]) < self.resolve(tokens[2]),
            'lessThanEquals' : self.resolve(tokens[0]) <= self.resolve(tokens[2]),
            'greaterThan' : self.resolve(tokens[0]) > self.resolve(tokens[2]),
            'greaterThanEquals' : self.resolve(tokens[0]) >= self.resolve(tokens[2]),
            'notEquals' : self.resolve(tokens[0]) != self.resolve(tokens[2]),
            'and' : self.resolve(tokens[2]) and self.resolve(tokens[0]),
            'or' : self.resolve(tokens[2]) or self.resolve(tokens[0])
        }.get(tokens[1], None)

    def resolve(self, value):
        value = value.lower()
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            e = core.Expression.Expression(value, self.call_stack, self.variables)
            return str(e.evaluate())


    def is_valid_answer(self, tokens):
            if len(tokens) > 1:
                return False
            else:
                return True