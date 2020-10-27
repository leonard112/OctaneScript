from core.Math import Math
from core.Fail import fail


class Expression:
    def __init__ (self, expression, line, variables):
        self.expression = expression
        self.line = line
        self.variables = variables
        self.error_type = "Expression Error"


    def evaluate (self):
        if self.expression == "":
            return ""

        tokens = self.parse_expression(self.expression, [])

        self.is_valid_expression(tokens)

        result = ""

        for token in tokens:
            token = token.lstrip()
            token = token.rstrip()
            
            if token[0] == '"' and token[-1] == '"':
                if token[1:-1].count('"') == 0:
                    result += token[1:-1]
                else:
                    fail("String contains double quotes.", self.error_type, self.line)
            elif token[0] == "'" and token[-1] == "'":
                if token[1:-1].count("'") == 0:
                    result += token[1:-1]
                else:
                    fail("String contains single quotes.", self.error_type, self.line)
            elif token[0] == "(" and token[-1] == ")":
                math_expression = Math(token, self.line, self.variables)
                result += math_expression.calculate()
            elif token == ".":
                None
            else:
                try:
                    result += self.get_variable(token)
                except:
                    try:
                        result += str(float(token))
                    except:
                        fail("Bad argument.", self.error_type, self.line)

        return result


    def parse_expression(self, expression, tokens):
        expression = expression.lstrip()
    
        if expression[0] == '"':
            next_occurance = expression[1:].find('"') + 1
            tail = expression[next_occurance + 1:]
            tokens += [expression[0:next_occurance+1]]
        elif expression[0] == "'":
            next_occurance = expression[1:].find("'") + 1
            tail = expression[next_occurance + 1:]
            tokens += [expression[0:next_occurance+1]]
        elif expression[0] == ".":
            tail = expression[1:]
            tokens += [expression[0]]
        elif expression[0] == "(":
            try:
                math_expression = self.parse_math_expression(expression, 0, -1, True)
            except:
                fail("Extra or missing parenteses.", self.error_type, self.line)
            tail = expression[len(math_expression):]
            tokens += [math_expression]
        else:
            variable = expression.split(' ', 1)[0].split('.', 1)[0]
            tail = expression[len(variable):]
            tokens += [variable]
        try:
            return self.parse_expression(tail, tokens)
        except:
            return tokens


    # pass '0' for parentheses_count
    # pass '-1' in for i
    # pass 'True' in for init
    def parse_math_expression(self, expression, parentheses_count, i, init):
        i += 1

        if parentheses_count == 0 and init == False:
            return expression[:i]
        if expression[i] == "(":
            return self.parse_math_expression(expression, parentheses_count + 1, i, False)
        elif expression[i] == ")":
            return self.parse_math_expression(expression, parentheses_count - 1, i, False)
        else:
            return self.parse_math_expression(expression, parentheses_count, i,  False)


    def is_valid_expression(self, expression):
        dot_count = expression.count(".")
        if dot_count * 2 != len(expression)-1:
            fail("Extra or missing '.', '\"', or \"'\".", self.error_type, self.line)

            
    def get_variable(self, variable):
        if variable in self.variables:
            return self.variables[variable]
                