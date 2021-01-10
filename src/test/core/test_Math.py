import pytest
from core.Line import Line
from core.Stack import Stack
from core.Math import Math
from Interpreter import reserved

line = Line("TEST", 0, "test")
test_stack = Stack()
test_stack.push(line)

# PARENTHESES
def test_no_parentheses_fails():
    assert_error(Math('1 + 1', test_stack, {}))
def test_no_right_parentheses_fails():
    assert_error(Math('(1 + 1', test_stack, {}))
def test_no_left_parentheses_fails():
    assert_error(Math('1 + 1)', test_stack, {}))
def test_extra_right_parentheses_fails():
    assert_error(Math('((1 + 1)', test_stack, {}))
def test_extra_left_parentheses_fails():
    assert_error(Math('(1 + 1))', test_stack, {}))
def test_extra_left_right_parentheses_equal_success():
    assert_success(Math('((1 + 1))', test_stack, {}))
def test_adding_two_separate_expressions_works():
    assert_success(Math('((1 + 1) + (1 + 1))', test_stack, {}))
def test_adding_three_separate_expressions_works():
    assert_success(Math('((1 + 1) + (1 + 1 + 1) + (1 + 1))', test_stack, {}))
def test_adding_four_separate_expressions_works():
    assert_success(Math('((1 + 1) + (1 + 1 + 1) + (1 + 1) + (1 + 1))', test_stack, {}))

def test_complex_missing_right_parentheses_fails():
    assert_error(Math('(1 + (2 * (2 ^ 3) * 2)', test_stack, {}))
def test_complex_missing_left_parentheses_fails():
    assert_error(Math('(1 + 2 * (2 ^ 3) * 2))', test_stack, {}))
def test_complex_extra_right_parentheses_fails():
    assert_error(Math('(1 + (2 * (2 ^ 3)) * 2))', test_stack, {}))
def test_complex_extra_left_parentheses_fails():
    assert_error(Math('(1 + ((2 * (2 ^ 3) * 2))', test_stack, {}))
def test_complex_extra_left_right_parentheses_sucess():
    assert_success(Math('(1 + ((2 * (2 ^ 3))) * 2)', test_stack, {}))

# OPERATIONS
def test_invalid_operation_fails():
    assert_error(Math('(1 x 1)', test_stack, {}))
def test_missing_operation_fails():
    assert_error(Math('(1 1)', test_stack, {}))
def test_addition_successful():
    assert Math('(1 + 1)', test_stack, {}).calculate() == "2.0"
def test_subtraction_successful():
    assert Math('(1 - 1)', test_stack, {}).calculate() == "0.0"
def test_multiplication_successful():
    assert Math('(3 * 2)', test_stack, {}).calculate() == "6.0"
def test_division_successful():
    assert Math('(10 / 2)', test_stack, {}).calculate() == "5.0"
def test_remainder_successful():
    assert Math('(10 % 2)', test_stack, {}).calculate() == "0.0"
def test_power_successful():
    assert Math('(2 ^ 4)', test_stack, {}).calculate() == "16.0"
def test_root_of_successful():
    assert Math('(2 rootOf 25)', test_stack, {}).calculate() == "5.0"
def test_commplex_valid_operation_successful():
    assert Math('(10 * 2 * ((1 + 1) rootOf 25) + 1)', test_stack, {}).calculate() == "101.0"
def test_three_separate_expressions_with_multiple_operations_works():
    assert Math('((4 ^ 2) + (2 * 4 / 2) - (1 + 1))', test_stack, {}).calculate() == "18.0"
def test_four_separate_expressions_with_multiple_operations_works():
    assert Math('((4 ^ 2) + (2 * 4 / 2) - (1 + 1) - (2 * 4))', test_stack, {}).calculate() == "10.0"

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


def assert_error(expression):
    with pytest.raises(SystemExit) as error:
            expression.calculate()
    assert error.type == SystemExit
    assert error.value.code == 1

def assert_success(expression):
    try:
        expression.calculate()
    except:
        pytest.fail()