# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

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
        expression = expression.strip()

        if len(expression) == 0:
            return tokens
        else:
            first_word = expression.split(' ', 1)[0].split(self.right_enclosing_symbol, 1)[0].split(".", 1)[0]
            # parse entire alpha words proceeded by space, right enclosing symbol, or "." operator
            if first_word.isalpha():
                first_word_length = len(first_word)
                rest_of_expression = expression[first_word_length:]
                # if word is following by . operator tokenize string expression
                if rest_of_expression.strip()[0] == ".":
                    token = self.parse_string_expression(expression)
                    token_length = len(token)
                    tokens += [token]
                    return self.parse_expression(expression[token_length:], tokens)
                elif first_word == "type":
                    token = first_word + " " + self.parse_string_expression(expression[first_word_length+1:])
                    token_length = len(token)
                    tokens += [token]
                    return self.parse_expression(expression[token_length:], tokens)
                tokens += [expression[0:first_word_length]]
                return self.parse_expression(expression[first_word_length:], tokens)
            else:
                if expression[0] == '"' or expression[0] == "'": # parse entire string expressions
                    token = self.parse_string_expression(expression)
                else: # parse expression symbols
                    token = self.tokenize_on_symbol(expression)
                token_length = len(token)
                tokens += [token]
                return self.parse_expression(expression[token_length:], tokens)


    def tokenize_on_symbol(self, expression):
        for symbol in self.symbols: # when expression currently starts with expression symbol
            symbol_length = len(symbol)
            if expression[0:symbol_length] == symbol:
                if symbol == "[" and expression.find(".") > expression.find("]"):
                    first_char_following_boolean = expression[expression.find(self.right_enclosing_symbol)+1:].lstrip()[0]
                    if first_char_following_boolean == ".":
                        token = self.parse_string_expression(expression)
                        if token.count("[") == token.count("]"):
                            return token
                return symbol
        token = expression
        for symbol in self.symbols: # when expression contains an expression symbol
            if symbol in expression:
                tokens = token.split(symbol, 1)
                token = tokens[0]
                after_token = None
                if len(tokens) > 1:
                    after_token = tokens[1]
                if symbol.isalpha() and after_token != None:
                    token = self.tokenize_on_alpha_symbol_after_initial_token(expression, symbol, token)
        return token


    def tokenize_on_alpha_symbol_after_initial_token(self, expression, symbol, token):
        symbol_index = expression.index(symbol)
        char_before_symbol = expression[symbol_index-1]
        symbol_length = len(symbol)
        if char_before_symbol.isalpha():
            token = token.split(symbol, 1)[0] + symbol
        if len(token)+symbol_length < len(expression):
            char_after_token = expression[symbol_index+symbol_length]
            if char_after_token.isalpha():
                expression_after_token = expression[symbol_index+len(symbol):]
                char_after_symbol_index = self.get_first_non_alpha_char_or_end(expression_after_token)
                char_after_token = expression[symbol_index+symbol_length+char_after_symbol_index]
                token = expression[:symbol_index+symbol_length+char_after_symbol_index]
            if char_after_token == ".":
                token = self.parse_string_expression(expression)
        if token.rstrip()[-1] == self.right_enclosing_symbol:
            token = token[:token.index(self.right_enclosing_symbol)]
        return token


    def parse_string_expression(self, expression):
        expression_no_white_space = expression.replace(" ", "")
        start_symbol = expression_no_white_space[0]
        if start_symbol == '"' or start_symbol == "'" or start_symbol == "(" or start_symbol == "[" or start_symbol == "<":
            token = ""
            if start_symbol == "(":
                token = expression[:expression.index(")")+1]
            elif start_symbol == "[":
                token = expression[:expression.index("]")+1]
            elif start_symbol == "<":
                token = expression[:expression.index(">")+1]
            else:
                try:
                    token = expression[:expression[1:].index(start_symbol)+2]
                except: # let erronious value bubble up to be handled later
                    token = expression
            if expression_no_white_space.find(".") == len(token.replace(" ", "")):
                partitions = self.split_string_expression_on_dot_operator(expression)
                return partitions[0] + self.parse_string_expression(partitions[1])
            if start_symbol == self.left_enclosing_symbol:
                return token
            return token.replace(self.right_enclosing_symbol, "")
        else:
            variable_token = expression.split(' ', 1)[0].split('.', 1)[0]
            rest_of_expression = expression[len(variable_token):]
            if len(rest_of_expression) > 0:
                if rest_of_expression.lstrip()[0] == ".":
                    partitions = self.split_string_expression_on_dot_operator(expression)
                    return partitions[0] + self.parse_string_expression(partitions[1])
            return expression.split(' ', 1)[0].replace(self.right_enclosing_symbol, "")


    def get_first_non_alpha_char_or_end(self, expression):
        for char in expression:
            if char.isalpha() == False:
                return expression.index(char)
        return -1

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