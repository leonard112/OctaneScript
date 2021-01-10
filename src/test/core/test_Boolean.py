import pytest
from core.Line import Line
from core.Stack import Stack
from core.Boolean import Boolean
from Interpreter import reserved

line = Line("TEST", 0, "test")
test_stack = Stack()
test_stack.push(line)

# Brackets
def test_no_brackets_fails():
    assert_error(Boolean('true', test_stack, {}))
def test_no_right_bracket_fails():
    assert_error(Boolean('[true', test_stack, {}))
def test_no_left_bracket_fails():
    assert_error(Boolean('true]', test_stack, {}))
def test_extra_right_bracket_fails():
    assert_error(Boolean('[[true]', test_stack, {}))
def test_extra_left_bracket_fails():
    assert_error(Boolean('[true]]', test_stack, {}))
def test_extra_left_right_brackets_equal_success():
    assert_success(Boolean('[[true]]', test_stack, {}))
def test_evaluating_two_separate_conditionals_works():
    assert_success(Boolean('[[true] and [true]]', test_stack, {}))
def test_evaluating_three_separate_conditionals_works():
    assert_success(Boolean('[[true] and [true] and [true]]', test_stack, {}))
def test_evaluating_four_separate_conditionals_works():
    assert_success(Boolean('[[true] and [true] and [true] and [true]]', test_stack, {}))

"""
def test_complex_missing_right_bracket_fails():
    assert_error(Math('[true equals [true notEquals [false and false] * 2)', test_stack, {}))
def test_complex_missing_left_parentheses_fails():
    assert_error(Math('(1 + 2 * (2 ^ 3) * 2))', test_stack, {}))
def test_complex_extra_right_parentheses_fails():
    assert_error(Math('(1 + (2 * (2 ^ 3)) * 2))', test_stack, {}))
def test_complex_extra_left_parentheses_fails():
    assert_error(Math('(1 + ((2 * (2 ^ 3) * 2))', test_stack, {}))
def test_complex_extra_left_right_parentheses_sucess():
    assert_success(Math('(1 + ((2 * (2 ^ 3))) * 2)', test_stack, {}))
"""

# OPERATIONS
def test_invalid_operation_fails():
    assert_error(Boolean('[true invalid true]', test_stack, {}))
def test_missing_operation_fails():
    assert_error(Boolean('[true true]', test_stack, {}))
# EQUALS
def test_equals_for_equal_values_true():
    assert Boolean('[1 equals 1]', test_stack, {}).evaluate() == True
    assert Boolean('[true equals true]', test_stack, {}).evaluate() == True
    assert Boolean('["hello" equals "hello"]', test_stack, {}).evaluate() == True
    assert Boolean('[x equals y]', test_stack, {'x': 1, 'y': 1}).evaluate() == True
def test_equals_for_unequal_values_false():
    assert Boolean('[1 equals 2]', test_stack, {}).evaluate() == False
# NOT EQUALS
def test_not_equals_for_unequal_values_true():
    assert Boolean('[1 notEquals 2]', test_stack, {}).evaluate() == True
def test_not_equals_for_equal_values_false():
    assert Boolean('[1 notEquals 1]', test_stack, {}).evaluate() == False
# LESS THAN
def test_less_than_for_first_less_than_following_true():
    assert Boolean('[1 lessThan 2]', test_stack, {}).evaluate() == True
def test_less_than_for_first_greater_than_following_false():
    assert Boolean('[2 lessThan 1]', test_stack, {}).evaluate() == False
def test_less_than_for_first_equal_to_following_false():
    assert Boolean('[1 lessThan 1]', test_stack, {}).evaluate() == False
#LESS THAN EQUALS
def test_less_than_equals_for_first_less_than_following_true():
    assert Boolean('[1 lessThanEquals 2]', test_stack, {}).evaluate() == True
def test_less_than_equals_for_first_greater_than_following_false():
    assert Boolean('[2 lessThanEquals 1]', test_stack, {}).evaluate() == False
def test_less_than_equals_for_first_equal_to_following_false():
    assert Boolean('[1 lessThanEquals 1]', test_stack, {}).evaluate() == True
# GREATER THAN
def test_greater_than_for_first_less_than_following_false():
    assert Boolean('[1 greaterThan 2]', test_stack, {}).evaluate() == False
def test_greater_than_for_first_greater_than_following_true():
    assert Boolean('[2 greaterThan 1]', test_stack, {}).evaluate() == True
def test_greater_than_for_first_equal_to_following_false():
    assert Boolean('[1 greaterThan 1]', test_stack, {}).evaluate() == False
# GREATER THAN EQUALS
def test_greater_than_equals_for_first_less_than_following_false():
    assert Boolean('[1 greaterThanEquals 2]', test_stack, {}).evaluate() == False
def test_greater_than_equals_for_first_greater_than_following_true():
    assert Boolean('[2 greaterThanEquals 1]', test_stack, {}).evaluate() == True
def test_greater_than_equals_for_first_equal_to_following_false():
    assert Boolean('[1 greaterThanEquals 1]', test_stack, {}).evaluate() == True
# AND
def test_true_and_true_is_true():
    assert Boolean('[true and true]', test_stack, {}).evaluate() == True
def test_true_and_false_is_false():
    assert Boolean('[true and false]', test_stack, {}).evaluate() == False
def test_false_and_true_is_false():
    assert Boolean('[false and true]', test_stack, {}).evaluate() == False
def test_false_and_false_is_false():
    assert Boolean('[false and false]', test_stack, {}).evaluate() == False
# OR
def test_true_or_true_is_true():
    assert Boolean('[true or true]', test_stack, {}).evaluate() == True
def test_true_or_false_is_true():
    assert Boolean('[true or false]', test_stack, {}).evaluate() == True
def test_false_or_true_is_true():
    assert Boolean('[false or true]', test_stack, {}).evaluate() == True
def test_false_or_false_is_false():
    assert Boolean('[false or false]', test_stack, {}).evaluate() == False

"""
# SPACING
def test_no_spaces_successful():
    assert_success(Math('(1+(2*(2^3))*2)', test_stack, {}))
def test_large_spaces_successful():
    assert_success(Math('(1  +  (  2  *  (  2  ^  3  ))  *  2  )', test_stack, {}))
def test_variable_spaces_successful():
    assert_success(Math('(1 + (  2  *  (2^3)) * 2)', test_stack, {})) 
def test_variable_spaces_successful():
    assert_success(Math('(1 + (  2  *  (2^3)) * 2)', test_stack, {}))

# VARIABLES
def test_math_using_valid_variable_successful():
    assert_success(Math('(1 + (x * (2 ^ y)) * 2)', test_stack, {'x': 2, 'y': 3}))
def test_math_using_invalid_variable_fails():
    assert_error(Math('(1 + ( x * (2 ^ y)) * 2)', test_stack, {'x': "string is no good", 'y': 3}))
"""

def assert_error(expression):
    with pytest.raises(SystemExit) as error:
            expression.evaluate()
    assert error.type == SystemExit
    assert error.value.code == 1

def assert_success(expression):
    try:
        expression.evaluate()
    except:
        pytest.fail()