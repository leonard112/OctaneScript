# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from core.Utilites import suppress_stdout_stderr
from core.Boolean import Boolean
from core.Math import Math
from core.Fail import fail
from Reserved import reserved


class Expression:
    def __init__ (self, expression, call_stack, variables):
        self.expression = expression
        self.call_stack = call_stack
        self.variables = variables
        self.error_type = "Expression Error"


    def evaluate (self):
        if self.expression == "":
            return ""
        elif self.expression == "array":
            return []
        elif self.expression[0] == "<" and self.expression[-1] == ">":
            return self.build_array(self.expression)

        tokens = self.parse_expression(self.expression, [])
        self.is_valid_expression(tokens)

        result = ""

        for token in tokens:
            token = token.strip()
            
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
                result += str(self.perform_type_conversion(math_expression.calculate()))
            elif token[0] == "[" and token[-1] == "]":
                boolean = Boolean(token, self.call_stack, self.variables)
                result += str(boolean.evaluate()).lower()

            elif token == ".":
                None
            else:
                token = self.resolve(token)
                if type(token) == list:
                    result += "<" + str(token)[1:-1] + ">"
                elif type(token) == bool:
                    result += str(token).lower()
                else:
                    result += str(token)
        return self.perform_type_conversion(result)
            

    def resolve(self, token):
        token = self.perform_type_conversion(token)
        if type(token) == str:
            if "<" in token and ">" in token:
                start_delimiter_index = token.find("<")
                array_name = token[:start_delimiter_index].strip()
                try:
                    array = self.variables[array_name]
                except Exception:
                    fail("\"" + array_name + "\" is undefined within the current scope.", self.error_type, self.call_stack)
                indicies = token[start_delimiter_index:]
                return self.get_array_element_or_subarray(token, array, indicies)
            else:
                try:
                    return self.variables[token]
                except Exception:
                    if token.split("(")[0] != token:
                        fail("The function \"" + token.split("(")[0] + "\" is undefined.", self.error_type, self.call_stack)
                    fail("The variable \"" + token + "\" is undefined within the current scope.", self.error_type, self.call_stack)
        else:
            return token


    def get_array_element_or_subarray(self, unparsed_expression, array, indicies):
        start_delimiter_index = indicies.find("<")
        end_delimiter_index = indicies.find(">")
        array_index_expression = indicies[start_delimiter_index + 1:end_delimiter_index].strip()
        if ":" in array_index_expression:
            array_index_expression_tokens = array_index_expression.split(":")
            if len(array_index_expression_tokens) != 2:
                fail(f"Extra ':' in subarray.", self.error_type, self.call_stack)
            start_index = array_index_expression_tokens[0]
            end_index = array_index_expression_tokens[1]
            if start_index == "start":
                start_index = 0
            elif start_index == "end":
                start_index = -1
            else:
                start_index = self.get_array_index_value(start_index)
            if end_index == "start":
                end_index = 0
            elif end_index == "end":
                end_index = len(array)
            else:
                end_index = self.get_array_index_value(end_index)
            if start_index > end_index:
                fail(f"Start array index cannot be greater than end array index.", self.error_type, self.call_stack)
            if end_index > len(array):
                fail(f"Start array index cannot be greater than the size of the array.", self.error_type, self.call_stack)
            if len(indicies) > end_delimiter_index + 1:
                return self.handle_nested_array_element_or_subarray(indicies, end_delimiter_index, unparsed_expression, array[start_index:end_index])
            try:
                return array[start_index:end_index]
            except:
                fail("The subarray \"" + unparsed_expression + "\" does not exist.", self.error_type, self.call_stack)
        if array_index_expression == "first" or array_index_expression == "peek":
            array_index = 0
        elif array_index_expression == "last":
            array_index = -1
        else:
            array_index = self.get_array_index_value(array_index_expression)
        if len(indicies) > end_delimiter_index + 1:
            return self.handle_nested_array_element_or_subarray(indicies, end_delimiter_index, unparsed_expression, array[array_index])
        try:
            return array[array_index]
        except:
            fail("The array element \"" + unparsed_expression + "\" does not exist.", self.error_type, self.call_stack)
    

    def get_array_index_value(self, array_index_expression):
        array_index = Expression(array_index_expression, self.call_stack, self.variables).evaluate()
        if type(array_index) != int:
            fail(f"Cannot get array element because the index '{array_index_expression}' is not an integer.", self.error_type, self.call_stack)
        if array_index < 0:
            fail(f"Array index cannot be less than 0.", self.error_type, self.call_stack)
        return array_index


    def handle_nested_array_element_or_subarray(self, indicies, end_delimiter_index, unparsed_expression, array):
        indicies = indicies[end_delimiter_index + 1:]
        if "<" not in indicies or ">" not in indicies:
            fail(f"Missing angle bracket.", self.error_type, self.call_stack)
        return self.get_array_element_or_subarray(unparsed_expression, array, indicies)


    def perform_type_conversion(self, token):
        if token == "true" or token == "True":
            return True
        elif token == "false" or token == "False":
            return False
        elif len(token) >= 2:
            if token[0] == "<" and token[-1] == ">":
                return self.build_array(token)
        try:
            return int(token)
        except:
            try:
                float_token = float(token)
                int_token = int(float_token)
                if float_token == int_token:
                    return int_token
                else:
                    return float_token
            except:
                return token.replace("\\n", "\n").replace("\\t", "\t")


    def parse_expression(self, expression, tokens):
        expression = expression.strip()
    
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
            if expression[0] == "<":
                non_string_token = expression.split('.', 1)[0]
            else:
                non_string_token = expression.split(' ', 1)[0].split('.', 1)[0]
            non_string_token_length = len(non_string_token)
            if "<" in non_string_token:
                if non_string_token[0] == "<" and ">" in expression:
                    try:
                        if tokens[-1] == ".":
                            non_string_token = expression[:expression.rindex('>')+1]
                            non_string_token_length = len(non_string_token)
                        else:
                            raise Exception
                    except:
                        try:
                            if tokens[-1] not in reserved:
                                non_string_token = tokens[-1] + " " + expression[:expression.rindex('>')+1]
                                tokens = tokens[:-1]
                                non_string_token_length = len(non_string_token)
                        except:
                            pass
                else:
                    try:
                        non_string_token = expression[:expression.rindex('>')+1]
                        non_string_token_length = len(non_string_token)
                    except:
                        pass
            if "(" in non_string_token and "<(" not in non_string_token:
                function_parameter_start = expression.find("(")
                expression_after_function_parameter_start = expression[function_parameter_start:]
                function_name = expression[:function_parameter_start]
                non_string_token = function_name + self.parse_specialized_expression(expression_after_function_parameter_start, 0, -1, "(", ")", True) + ","
                non_string_token_length = len(non_string_token)
                if len(expression) >= non_string_token_length:
                    if expression[non_string_token_length-1] == ">":
                        non_string_token = non_string_token[:-1] + ">"
                else:
                    non_string_token = non_string_token[:-1]
            non_string_token_type = self.perform_type_conversion(non_string_token)
            tail = expression[non_string_token_length:]
            if type(non_string_token_type) == int and len(tail) > 0:
                if tail[0] == ".":
                    non_string_token = non_string_token + "." + tail[1:].split(' ', 1)[0].split('.', 1)[0]
                    tail = expression[len(non_string_token):]
            elif "(" in non_string_token and ")" in non_string_token and non_string_token[-1] == ",":
                non_string_token = non_string_token[:-1]
                tail = expression[len(non_string_token):]
            tokens += [non_string_token]
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


    def build_array(self, array):
        self.ensure_array_does_not_have_extra_commas(array)
        array = array[1:-1]
        array = array.strip()
        try: # check if array is actually a boolean
            if " " not in array:
                raise Exception
            boolean = Boolean("[" + array + "]", self.call_stack, self.variables)
            with suppress_stdout_stderr():
                return boolean.evaluate()
        except:
            if array.count('<') != array.count('>'):
                fail("Extra or missing '<', or '>'.", self.error_type, self.call_stack)
            array = array.replace("[", "[<").replace("]", ">[")
            array_tokens = array.split("[")
            array_tokens = ' '.join(array_tokens).split(",")
            array_object = []
            array_tokens = self.reconcatenate_nested_object(array_tokens, "<", ">")
            array_tokens = self.reconcatenate_nested_object(array_tokens, "'", "'")
            for array_token in array_tokens:
                array_token = array_token.strip()
                expression = Expression(array_token, self.call_stack, self.variables)
                array_object.append(expression.evaluate())
            return array_object


    def reconcatenate_nested_object(self, array_tokens, start_delimiter, end_delimiter):
        start_delimiter_count = 0
        end_delimiter_count = 0
        result_array_tokens = []
        concatenated_element = ""
        for token in array_tokens:
            token = token.strip()
            if token != "":
                if len(token) != 0:
                    start_delimiter_count += token.count(start_delimiter)
                    end_delimiter_count += token.count(end_delimiter)
                if start_delimiter_count == end_delimiter_count:
                    if concatenated_element != "":
                        token = concatenated_element + token
                        concatenated_element = ""
                    result_array_tokens.append(token)
                else:
                    concatenated_element += token + ", "
        return result_array_tokens

    
    def ensure_array_does_not_have_extra_commas(self, array):
        array = array.replace(' ','')
        if "<," in array or ",>" in array or ",," in array:
            fail("Extra comma in array definition.", self.error_type, self.call_stack)