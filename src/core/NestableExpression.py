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
            return tokens
        else:
            first_word = expression.split(' ', 1)[0].split(self.right_enclosing_symbol, 1)[0]
            if first_word.isalpha(): # parse entire alpha words proceeded by space or right enclosing symbol
                first_word_length = len(first_word)
                rest_of_expression = expression[first_word_length:]
                if rest_of_expression.lstrip()[0] == ".":
                    token = self.parse_string_expression(expression)
                    token_length = len(token)
                    tokens += [token]
                    return self.parse_expression(expression[token_length:], tokens)
                tokens += [expression[0:first_word_length]]
                return self.parse_expression(expression[first_word_length:], tokens)
            elif expression[0] == '"' or expression[0] == "'": # parse entire string values
                token = self.parse_string_expression(expression)
                token_length = len(token)
                tokens += [token]
                return self.parse_expression(expression[token_length:], tokens)
            else: # parse expression symbols
                for symbol in self.symbols: # when expression currently starts with expression symbol
                    symbol_length = len(symbol)
                    if expression[0:symbol_length] == symbol:
                        tokens += [expression[0:symbol_length]]
                        return self.parse_expression(expression[symbol_length:], tokens)
                token = expression
                for symbol in self.symbols: # when expression does not start with expression symbol but contains them
                    if symbol in expression:
                        token = token.split(symbol, 1)[0]
                token_length = len(token)
                tokens += [expression[0:token_length]]
                return self.parse_expression(expression[token_length:], tokens)


    def parse_string_expression(self, expression):
        expression_no_white_space = expression.replace(" ", "")
        start_symbol = expression_no_white_space[0]
        if start_symbol == '"' or start_symbol == "'":
            string = expression[:expression[1:].index(start_symbol)+2]
            if expression_no_white_space.find(".") == len(string):
                partitions = self.split_string_expression_on_dot_operator(expression)
                return partitions[0] + self.parse_string_expression(partitions[1])
            return string.replace(self.right_enclosing_symbol, "")
        else:
            variable_token = expression.split(' ', 1)[0]
            rest_of_expression = expression[len(variable_token):]
            if len(rest_of_expression) > 0:
                if rest_of_expression.lstrip()[0] == ".":
                    partitions = self.split_string_expression_on_dot_operator(expression)
                    return partitions[0] + self.parse_string_expression(partitions[1])
            return expression.split(' ', 1)[0].replace(self.right_enclosing_symbol, "")


    def split_string_expression_on_dot_operator(self, expression):
        dot_index = expression.find(".")
        expression_after_dot = expression[dot_index+1:].lstrip()
        expression_start = self.get_first_string_token_up_to_and_including_dot_operator(expression, dot_index)
        return [expression_start, expression_after_dot]

    def get_first_string_token_up_to_and_including_dot_operator(self, expression, dot_index):
        next_token_starting_char = expression[dot_index+1:].lstrip()[0]
        next_token_starting_char_index = expression[dot_index:].index(next_token_starting_char) + dot_index
        return expression[:next_token_starting_char_index]


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