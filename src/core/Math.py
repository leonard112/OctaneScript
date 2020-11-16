from core.Fail import fail


class Math:
    def __init__ (self, expression, call_stack, variables):
        self.expression = expression
        self.call_stack = call_stack
        self.variables = variables
        self.error_type = "Math Error"
        self.math_symbols = ['(', '+', '-', '*', '/', '%', '^', 'rootOf', ')']


    def calculate(self):
        if self.expression[0] != "(" and self.expression[-1] != ")":
            fail("Extra or missing parentheses.", self.error_type, self.call_stack)
        return self.calculate_recursive(self.parse_math_expression(self.expression, []))[0]


    def calculate_recursive(self, expression):
        left_parentheses_count = expression.count("(")
        right_parentheses_count = expression.count(")")

        if left_parentheses_count == right_parentheses_count:
            if left_parentheses_count > 0:
                left_parentheses_index = expression.index("(")
                right_parentheses_index = len(expression) - expression[::-1].index(")") - 1

                outside_left = expression[:left_parentheses_index]
                outside_right = expression[right_parentheses_index+1:]
                sub_expression = expression[left_parentheses_index+1:right_parentheses_index]

                new_expression = outside_left + self.calculate_recursive(sub_expression) + outside_right
                return self.evaluate_all(new_expression)

            return self.evaluate_all(expression)
        
        else:
            fail("Extra or missing parentheses.", self.error_type, self.call_stack)


    def parse_math_expression(self, expression, tokens):
        expression = expression.lstrip()

        if len(expression) == 0:
            return tokens
        else:
            if expression[0] == "(":
                tokens += [expression[0]]
                return self.parse_math_expression(expression[1:], tokens)
            elif expression[0] == ")":
                tokens += [expression[0]]
                return self.parse_math_expression(expression[1:], tokens)
            elif expression[0] == "+":
                tokens += [expression[0]]
                return self.parse_math_expression(expression[1:], tokens)
            elif expression[0] == "-":
                tokens += [expression[0]]
                return self.parse_math_expression(expression[1:], tokens)
            elif expression[0] == "*":
                tokens += [expression[0]]
                return self.parse_math_expression(expression[1:], tokens)
            elif expression[0] == "/":
                tokens += [expression[0]]
                return self.parse_math_expression(expression[1:], tokens)
            elif expression[0] == "%":
                tokens += [expression[0]]
                return self.parse_math_expression(expression[1:], tokens)
            elif expression[0] == "^":
                tokens += [expression[0]]
                return self.parse_math_expression(expression[1:], tokens)
            elif expression[0:6] == "rootOf":
                tokens += [expression[0:6]]
                return self.parse_math_expression(expression[6:], tokens)
            else:
                current_token = expression.split(' ', 1)[0]
                for symbol in self.math_symbols:
                    current_token = current_token.split(symbol, 1)[0]

                tokens += [current_token]
                token_length = len(current_token)
                return self.parse_math_expression(expression[token_length:], tokens)

        
    def evaluate_all(self, tokens):
        if len(tokens) > 3:
            return self.evaluate_all(self.evaluate_single_operation(tokens[0:3]) + tokens[3:])
        elif len(tokens) == 3:
            return self.evaluate_single_operation(tokens[0:3])
        else:
            if self.is_valid_answer(tokens):
                return tokens
            fail("Missing or extra operator.", self.error_type, self.call_stack)


    def evaluate_single_operation(self, tokens):
        value = self.expression_switch(tokens)
        if value == None:
            fail("Invalid math operation.", self.error_type, self.call_stack)
        return [str(value)]


    def expression_switch(self, tokens):
        return {
            '+' : self.resolve(tokens[0]) + self.resolve(tokens[2]),
            '-' : self.resolve(tokens[0]) - self.resolve(tokens[2]),
            '*' : self.resolve(tokens[0]) * self.resolve(tokens[2]),
            '/' : self.resolve(tokens[0]) / self.resolve(tokens[2]),
            '%' : self.resolve(tokens[0]) % self.resolve(tokens[2]),
            '^' : self.resolve(tokens[0]) ** self.resolve(tokens[2]),
            'rootOf' : self.resolve(tokens[2]) ** (1/self.resolve(tokens[0]))
        }.get(tokens[1], None)


    def resolve(self, value):
        try:
            return float(value)
        except:
            try:
                return float(self.get_variable(value))
            except:
                fail("Math operations can only be performed with numbers", self.error_type, self.call_stack)


    def get_variable(self, variable):
        if variable in self.variables:
            return self.variables[variable]
    

    def is_valid_answer(self, tokens):
        if len(tokens) > 1:
            return False
        
        try:
            float(tokens[0])
            return True
        except:
            return False