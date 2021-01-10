from core.Boolean import Boolean
from core.Math import Math
from core.Fail import fail


class Expression:
    def __init__ (self, expression, call_stack, variables):
        self.expression = expression
        self.call_stack = call_stack
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
                    fail("String contains double quotes.", self.error_type, self.call_stack)
            elif token[0] == "'" and token[-1] == "'":
                if token[1:-1].count("'") == 0:
                    result += token[1:-1]
                else:
                    fail("String contains single quotes.", self.error_type, self.call_stack)
            elif token[0] == "(" and token[-1] == ")":
                math_expression = Math(token, self.call_stack, self.variables)
                result += math_expression.calculate()
            elif token[0] == "[" and token[-1] == "]":
                boolean = Boolean(token, self.call_stack, self.variables)
                result += str(boolean.evaluate()).lower()
            elif token == ".":
                None
            else:
                try:   
                    if len(tokens) == 1:
                        if token == "true":
                            return token
                        elif token == "false":
                            return token
                        else:
                            variable = self.variables[token]
                            if variable == True:
                                return "true"
                            elif variable == False:
                                return "false"
                            else:
                                return variable
                except:
                    try:
                        number = float(token)
                        if number == int(number):
                            result += str(int(number))
                        else:
                            result += str(int(number))
                    except:
                        fail("Bad argument.\n\nDefined variables: " + self.defined_variables_to_string(), self.error_type, self.call_stack)
        try:
            result = float(result)
            if result == int(result):
                return int(result)
            return result
        except:
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
                math_expression = self.parse_specialized_expression(expression, 0, -1, "(", ")", True)
            except:
                fail("Extra or missing parentheses on math expression.", self.error_type, self.call_stack)
            tail = expression[len(math_expression):]
            tokens += [math_expression]
        elif expression[0] == "[":
            try:
                boolean = self.parse_specialized_expression(expression, 0, -1, "[", "]", True)
            except:
                fail("Extra or missing bracket on boolean expression.", self.error_type, self.call_stack)
            tail = expression[len(boolean):]
            tokens += [boolean]
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
    def parse_specialized_expression(self, expression, parentheses_count, i, start_parentheses_type, end_parentheses_type, init):
        i += 1

        if parentheses_count == 0 and init == False:
            return expression[:i]
        if expression[i] == start_parentheses_type:
            return self.parse_specialized_expression(expression, parentheses_count + 1, i, start_parentheses_type, end_parentheses_type, False)
        elif expression[i] == end_parentheses_type:
            return self.parse_specialized_expression(expression, parentheses_count - 1, i, start_parentheses_type, end_parentheses_type, False)
        else:
            return self.parse_specialized_expression(expression, parentheses_count, i, start_parentheses_type, end_parentheses_type, False)


    def is_valid_expression(self, expression):
        dot_count = expression.count(".")
        if dot_count * 2 != len(expression)-1:
            fail("Extra or missing '.', '\"', or \"'\".", self.error_type, self.call_stack)

            
    def defined_variables_to_string(self):
        variables = ""
        for variable in self.variables:
            variables += "( " + variable + " : " + str(self.variables[variable]) + " ), "
        if variables == "":
            return "(None)"
        return variables[:-2]
                