# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from core.NestableExpression import NestableExpression
from core.Fail import fail


class Math(NestableExpression):
    def __init__ (self, expression, call_stack, variables):
        self.expression = expression
        self.call_stack = call_stack
        self.variables = variables
        self.error_type = "Math Error"
        self.right_enclosing_symbol = ")"
        self.left_enclosing_symbol = "("
        self.symbols = ['(', ')', '+', '-', '*', '/', '%', '^', 'rootOf']


    def calculate(self):
        if self.expression[0] != "(" or self.expression[-1] != ")":
            fail("Extra or missing parentheses.", self.error_type, self.call_stack)
        return self.evaluate_nestable_expression(self.parse_expression(self.expression, []), 
                                                 self.perform_operation)[0]


    def perform_operation(self, tokens):
        operator = tokens[1]
        operand_1 = self.resolve(tokens[0])
        operand_2 = self.resolve(tokens[2])
        if operator == '+': 
            return operand_1 + operand_2
        elif operator =='-': 
            return operand_1 - operand_2
        elif operator == '*': 
            return operand_1 * operand_2
        elif operator == '/': 
            try:
                return operand_1 / operand_2
            except:
                fail("Cannot divide by 0.", self.error_type, self.call_stack)
        elif operator == '%': 
            try:
                return operand_1 % operand_2
            except:
                fail("Cannot divide by 0.", self.error_type, self.call_stack)
        elif operator == '^': 
            return operand_1 ** operand_2
        elif operator == 'rootOf':
            try: 
                return operand_2 ** (1/operand_1)
            except:
                fail("Cannot take 0 root.", self.error_type, self.call_stack)


    def resolve(self, value):
        try:
            return float(value)
        except:
            try:
                return float(self.get_variable(value))
            except Exception:
                fail(f"Math operations can only be performed with numbers. '{value}' is not a number.", self.error_type, self.call_stack)


    def is_valid_answer(self, tokens):
            if len(tokens) > 1:
                return False
            
            try:
                float(tokens[0])
                return True
            except:
                return False

    
    def get_variable(self, variable):
        if variable in self.variables:
            return self.variables[variable]