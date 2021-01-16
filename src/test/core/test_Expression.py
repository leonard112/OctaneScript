# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import pytest
from core.Line import Line
from core.Stack import Stack
from core.Expression import Expression
from Reserved import reserved

line = Line("TEST", 0, "test")
test_stack = Stack()
test_stack.push(line)

# STRING EVALUATION
def test_no_quotes_fails():
    assert_error(Expression('test', test_stack, {}))
def test_no_leading_quote_fails():
    assert_error(Expression('test"', test_stack, {}))
def test_no_trailing_quote_fails():
    assert_error(Expression('"test', test_stack, {}))
def test_enclosed_in_double_quotes_successful():
    assert Expression('"test"', test_stack, {}).evaluate() == "test"
def test_enclosed_in_single_quotes_sucessful():
    assert Expression("'test'", test_stack, {}).evaluate() == "test"

# STRING CONCATENATION
def test_missing_dot_fails():
    assert_error(Expression('"test" "test"', test_stack, {}))
def test_bad_delimiter_fails():
    assert_error(Expression('"test" + "test"', test_stack, {}))
    assert_error(Expression('"test" x "test"', test_stack, {}))
def test_leading_dot_fails():
    assert_error(Expression('. "test" . "test"', test_stack, {}))
def test_trailing_dot_fails():
    assert_error(Expression('"test" . "test" .', test_stack, {}))
def test_vaid_concatenation_successful():
    assert Expression('"test" . "test"', test_stack, {}).evaluate() == "testtest"
    assert Expression('"test" . "test" . "test"', test_stack, {}).evaluate() == "testtesttest"
def test_uppercase_left_alone():
    assert Expression('"test" . "Test" . "TEST"', test_stack, {}).evaluate() == "testTestTEST"
def test_valid_concanenation_with_varying_white_space_successful():
    assert Expression('"test"."test"."test"', test_stack, {}).evaluate() == "testtesttest"
    assert Expression('"test" ."test"    .    "test"', test_stack, {})
def test_math_can_be_concatenated_with_strings():
    assert Expression('"test". (1 + 1)', test_stack, {}).evaluate() == "test2"
def test_numbers_can_be_concatenated_with_strings():
    assert Expression('"test". 5', test_stack, {}).evaluate() == "test5"
def test_booleans_can_be_concatenated_with_strings():
    assert Expression('"test". [true]', test_stack, {}).evaluate() == "testtrue"

# NUMBERS
def test_integer_no_parenthesis_returns_integer():
    assert Expression('5', test_stack, {}).evaluate() == 5
def test_integer_with_parenthesis_returns_integer():
    assert Expression('(5)', test_stack, {}).evaluate() == 5
def test_decimal_no_parenthesis_returns_decimal():
    assert Expression('3.33', test_stack, {}).evaluate() == 3.33
def test_decimal_with_parenthesis_returns_decimal():
    assert Expression('(3.33)', test_stack, {}).evaluate() == 3.33

# MATH
def test_math_expression_no_parenthesis_fails():
    assert_error(Expression('1 + 1', test_stack, {}))
def test_valid_math_exptression_returns_integer_result():
    assert Expression('(1 + 1)', test_stack, {}).evaluate() == 2
def test_valid_math_exptression_returns_decimal_result():
    assert Expression('(1 + 1.2)', test_stack, {}).evaluate() == 2.2

# BOOLEAN
def test_true_evaluates_to_true_no_brackets():
    assert Expression('true', test_stack, {}).evaluate() == True
def test_true_evaluates_to_true_with_brackets():
    assert Expression('[true]', test_stack, {}).evaluate() == True
def test_false_evaluates_to_false_no_brackets():
    assert Expression('false', test_stack, {}).evaluate() == False
def test_false_evaluates_to_false_with_brackets():
    assert Expression('[false]', test_stack, {}).evaluate() == False
def test_complex_true_evaluates_to_true_with_brackets():
    assert Expression('[true equals true]', test_stack, {}).evaluate() == True
def test_complex_false_evaluates_to_false_with_brackets():
    assert Expression('[false equals true]', test_stack, {}).evaluate() == False


# VARIABLES
def test_not_found_fails():
    assert_error(Expression('x', test_stack, {}))
def test_reserved_fails():
    for word in reserved:
        if word != "true" and word != "false":
            assert_error(Expression(word, test_stack, {}))
def test_string_value_can_be_resolved_from_variable():
    assert Expression('x', test_stack, {'x' : 'value'}).evaluate() == "value"
def test_integer_value_can_be_resolved_from_variable():
    assert Expression('x', test_stack, {'x' : 5}).evaluate() == 5
def test_decimal_value_can_be_resolved_from_variable():
    assert Expression('x', test_stack, {'x' : 5.5}).evaluate() == 5.5
def test_boolean_value_can_be_resolved_from_variable():
    assert Expression('x', test_stack, {'x' : True}).evaluate() == True
def test_string_can_be_concatenated_to_string_variable():
    assert Expression('"test" . x', test_stack, {'x' : 'value'}).evaluate() == "testvalue"
def test_string_can_be_concatenated_to_integer_number_variable():
    assert Expression('"test" . x', test_stack, {'x' : 5}).evaluate() == "test5"
def test_string_can_be_concatenated_to_decimal_number_variable():
    assert Expression('"test" . x', test_stack, {'x' : 5.5}).evaluate() == "test5.5"
def test_string_can_be_concatenated_to_boolean_variable():
    assert Expression('"test" . x', test_stack, {'x' : True}).evaluate() == "testtrue"
def test_valid_complex_expression_successful():
    assert Expression(
        '"hello " . x . \' this expression is valid. Here is y \' . y', test_stack,
        {'x' : 'xValue', 'y' : 'yValue'}
    ).evaluate() == "hello xValue this expression is valid. Here is y yValue"


def assert_error(expression):
    with pytest.raises(SystemExit) as error:
            expression.evaluate()
    assert error.type == SystemExit
    assert error.value.code == 1