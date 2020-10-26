import nltk
from core.Fail import fail

class Math:
    def __init__ (self, expression, line, variables):
        self.expression = expression
        self.line = line
        self.variables = variables
        self.error_type = "Math Error"

    def calculate(self):
        return self.calculate_recursive(self.expression)

    def calculate_recursive(self, expression):
        left_parentheses_count = expression.count("(")
        right_parentheses_count = expression.count(")")

        if left_parentheses_count == right_parentheses_count:
            if left_parentheses_count > 0:
                left_parentheses_index = expression.find("(")
                right_parentheses_index = len(expression) - expression[::-1].find(")") - 1

                outside_left = expression[:left_parentheses_index]
                outside_right = expression[right_parentheses_index+1:]
                sub_expression = expression[left_parentheses_index+1:right_parentheses_index]

                new_expression = outside_left + str(self.calculate_recursive(sub_expression)) +  outside_right

                return self.evaluate_all(nltk.word_tokenize(new_expression))

            return self.evaluate_all(nltk.word_tokenize(expression))
        
        else:
            fail("Extra or missing parentheses.", self.error_type, self.line)
        
    def evaluate_all(self, tokens):
        if len(tokens) > 3:
            return self.evaluate_all([str(self.evaluate_single_operation(tokens[0:3]))] + tokens[3:])
        return self.evaluate_single_operation(tokens[0:3])

    def evaluate_single_operation(self, tokens):
        if tokens[1] == "+":
            return self.resolve(tokens[0]) + self.resolve(tokens[2])
        elif tokens[1] == "-":
            return self.resolve(tokens[0]) - self.resolve(tokens[2])
        elif tokens[1] == "*":
            return self.resolve(tokens[0]) * self.resolve(tokens[2])
        elif tokens[1] == "/":
            return self.resolve(tokens[0]) / self.resolve(tokens[2])
        elif tokens[1] == "%":
            return self.resolve(tokens[0]) % self.resolve(tokens[2])
        elif tokens[1] == "^":
            return self.resolve(tokens[0]) ** self.resolve(tokens[2])
        elif tokens[1] == "rootOf":
            return self.resolve(tokens[2]) ** (1/self.resolve(tokens[0]))
    def resolve(self, value):
        try:
            return float(value)
        except:
            try:
                return float(self.get_variable(value))
            except:
                fail("Math operations can only be performed with numbers", self.error_type, self.line)

    def get_variable(self, variable):
        if variable in self.variables:
            return self.variables[variable]
        fail("Math operations can only be performed with numbers", self.error_type, self.line)