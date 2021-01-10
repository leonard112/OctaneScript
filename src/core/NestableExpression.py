# IMPORTANT: This is only intended to be used as a base class

from core.Fail import fail

class NestableExpression:
    def __init__ (self, expression, call_stack, variables):
        self.expression = expression
        self.call_stack = call_stack
        self.variables = variables
        self.error_type = "Nestable Expresion Error"
        self.right_enclosing_symbol = ""
        self.left_enclosing_symbol = ""
        self.symbols = []


    def parse_expression(self, expression, tokens):
        expression = expression.lstrip()

        if len(expression) == 0:
            return self.detokenize_operands(tokens)
        else:
            for symbol in self.symbols:
                symbol_length = len(symbol)
                if expression[0:symbol_length] == symbol:
                    tokens += [expression[0:symbol_length]]
                    return self.parse_expression(expression[symbol_length:], tokens)
        current_token = expression.split(' ', 1)[0]
        if current_token[0] != '"' and current_token[0] != "'":
            for symbol in self.symbols:
                current_token = current_token.split(symbol, 1)[0]
        else:
            if current_token[0] == '"':
                current_token = current_token[:current_token[1:].find('"')+2]
            else:
                current_token = current_token[:current_token[1:].find("'")+2]

        tokens += [current_token]
        token_length = len(current_token)
        return self.parse_expression(expression[token_length:], tokens)


    def detokenize_operands(self, tokens):
        if len(tokens) == 0 or len(tokens) == 1:
            return tokens
        elif tokens[0] not in self.symbols and tokens[1] not in self.symbols:
            return self.detokenize_operands([tokens[0] + " " + tokens[1]] + tokens[2:])
        
        else:
            return [tokens[0]] + self.detokenize_operands(tokens[1:])


    def evaluate_nestable_expression(self, expression, single_operation_evaluator):
        left_enclosing_symbol_count = expression.count(self.left_enclosing_symbol)
        right_enclosing_symbol_count = expression.count(self.right_enclosing_symbol)
        if left_enclosing_symbol_count == right_enclosing_symbol_count:

            if left_enclosing_symbol_count > 0:
                new_expression = []
                left_enclosing_symbol_index = expression.index(self.left_enclosing_symbol)
                right_enclosing_symbol_index = len(expression) - expression[::-1].index(self.right_enclosing_symbol) - 1
                
                if left_enclosing_symbol_index > right_enclosing_symbol_index:
                    outside_left = expression[:right_enclosing_symbol_index]
                    evaluated_outside_left = self.evaluate_nestable_expression(outside_left, single_operation_evaluator)
                    outside_right = expression[left_enclosing_symbol_index+1:]
                    evaluated_outside_right = self.evaluate_nestable_expression(outside_right, single_operation_evaluator)
                    intermediate_expression = expression[right_enclosing_symbol_index+1:left_enclosing_symbol_index]
                    new_expression = evaluated_outside_left + intermediate_expression + evaluated_outside_right
                else:
                    outside_left = expression[:left_enclosing_symbol_index]
                    outside_right = expression[right_enclosing_symbol_index+1:]
                    sub_expression = expression[left_enclosing_symbol_index+1:right_enclosing_symbol_index]

                    evaluated_sub_expression = self.evaluate_nestable_expression(sub_expression, single_operation_evaluator)
                    new_expression = outside_left + evaluated_sub_expression + outside_right
                return self.evaluate_nestable_expression(new_expression, single_operation_evaluator)
            return self.evaluate_all(expression, single_operation_evaluator)
            
        else:
            fail("Extra or missing enclosing symbol.", self.error_type, self.call_stack)


    def evaluate_all(self, tokens, single_operation_evaluator):
        if len(tokens) > 3:
            return self.evaluate_all(self.evaluate_single_operation(tokens[0:3], single_operation_evaluator) + 
                                                               tokens[3:], single_operation_evaluator)
        elif len(tokens) == 3:
            return self.evaluate_single_operation(tokens[0:3], single_operation_evaluator)
        else:
            if self.is_valid_answer(tokens):
                return tokens
            fail("Missing or extra operator.", self.error_type, self.call_stack)


    def evaluate_single_operation(self, tokens, single_operation_evaluator):
            value = single_operation_evaluator(tokens)
            if value == None:
                fail("Invalid operation", self.error_type, self.call_stack)
            return [str(value)]