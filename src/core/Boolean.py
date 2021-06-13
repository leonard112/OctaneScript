# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import core.Expression
from core.NestableExpression import NestableExpression
import core.Printer
from core.Fail import fail

class Boolean(NestableExpression):
    def __init__ (self, expression, call_stack, variables):
        self.expression = expression
        self.call_stack = call_stack
        self.variables = variables
        self.right_enclosing_symbol = "]"
        self.left_enclosing_symbol = "["
        self.error_type = "Boolean Error"
        self.symbols = ["[", "]", "lessThanEquals", "greaterThanEquals", "lessThan", "greaterThan", 
                        "equals", "notEquals", "and", "or", "true", "false"]


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
        try:
            token_1 = self.resolve(tokens[0].strip())
            token_2 = self.resolve(tokens[2].strip())
            return {
                'equals' : token_1 == token_2,
                'lessThan' : token_1 < token_2,
                'lessThanEquals' : token_1 <= token_2,
                'greaterThan' : token_1 > token_2,
                'greaterThanEquals' : token_1 >= token_2,
                'notEquals' : token_1 != token_2,
                'and' : self.perform_and_or(token_1, token_2, "and"),
                'or' : self.perform_and_or(token_1, token_2, "or")
            }.get(tokens[1], None)
        except Exception:
            fail("Differing value types cannot be compared.\n\t\t" +
                 "Operand 1: " + self.stringify_token(token_1) + "\n\t\t" +
                 "Operand 2: " + self.stringify_token(token_2), self.error_type, self.call_stack)


    def stringify_token(self, token):
        if type(token) == list:
            p = core.Printer.Printer("print", "", self.call_stack, self.variables)
            return p.stringify_array(token)
        return str(token)


    def perform_and_or(self, operand_1, operand_2, operator):
        if type(operand_1) != bool:
            operand_1 = True
        if type(operand_2) != bool:
            operand_2 = True
        if operator == "and":
            return operand_1 and operand_2
        if operator == "or":
            return operand_1 or operand_2
        raise Exception


    def resolve(self, value):
        value = value.lower()
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            try:
                return float(value)
            except:
                e = core.Expression.Expression(value, self.call_stack, self.variables)
                value = e.evaluate()
                if type(value) == list:
                    return value
                try:
                    return float(value)
                except:
                    return '"' + str(value) + '"'


    def is_valid_answer(self, tokens):
            if len(tokens) > 1:
                return False
            elif self.starts_and_ends_with_valid_symbols(tokens) == True:
                e = core.Expression.Expression(tokens[0], self.call_stack, self.variables)
                e.evaluate()
                return True
            elif tokens[0].lower() == "true" or tokens[0].lower() == "false":
                return True
            else:
                try:
                    float(tokens[0])
                    return True
                except:
                    try:
                        self.variables[tokens[0]]
                        return True
                    except:
                        return False


    def starts_and_ends_with_valid_symbols(self, tokens):
        start_symbol = tokens[0][0]
        end_symbol = tokens[0][-1]
        if start_symbol == '"' and end_symbol == '"':
            return True
        elif start_symbol == "'" and end_symbol == "'":
            return True
        elif start_symbol == "(" and end_symbol == ")":
            return True
        elif start_symbol == "<" and end_symbol == ">":
            return True
        return False