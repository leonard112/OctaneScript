# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import pytest
from core.Line import Line
from core.Stack import Stack
from core.Function import Function
from Interpreter import reserved

line = Line("TEST", 0, "test")
test_stack = Stack()
test_stack.push(line)


# FUNCTION DEFINITION
def test_valid_function_definition_constructs_function_properly():
    b = Function('testFunc(x, y, z)', test_stack, 0)
    assert b.function_variables == {'x' : None, 'y' : None, 'z' : None}
    assert b.function_start == 0
def test_missing_comma_in_function_definition_raises_error():
    assert_error_on_init("testFunc(x, y z)")
def test_extra_leading_comma_in_function_definition_raises_error():
    assert_error_on_init("testFunc(,x, y, z)")
def test_extra_trailing_comma_in_function_definition_raises_error():
    assert_error_on_init("testFunc(x, y, z,)")
def test_missing_leading_parenthesis_in_function_definition_raises_error():
    assert_error_on_init("testFuncx, y, z)")
def test_missing_trailing_parenthesis_in_function_definition_raises_error():
    assert_error_on_init("testFunc(x, y, z")
def test_extra_leading_parenthesis_in_function_definition_raises_error():
    assert_error_on_init("testFunc((x, y, z)")
def test_extra_trailing_parenthesis_in_function_definition_raises_error():
    assert_error_on_init("testFunc(x, y, z))")
def test_passing_in_double_quote_string_value_as_parameter_in_function_definition_raises_error():
    assert_error_on_init('testFunc(x, "hello", z)')
def test_passing_in_single_quote_string_value_as_parameter_in_function_definition_raises_error():
    assert_error_on_init("testFunc(x, 'hello', z)")
def test_passing_in_integer_value_as_parameter_in_function_definition_raises_error():
    assert_error_on_init("testFunc(x, 5, z)")
def test_passing_in_decimal_value_as_parameter_in_function_definition_raises_error():
    assert_error_on_init("testFunc(x, 5.3, z)")
def test_passing_in_math_as_parameter_in_function_definition_raises_error():
    assert_error_on_init("testFunc(x, (1 + 1), z)")
def test_passing_in_boolean_as_parameter_in_function_definition_raises_error():
    assert_error_on_init("testFunc(x, [true], z)")


def assert_error_on_init(function_definition):
    with pytest.raises(SystemExit) as error:
        Function(function_definition, test_stack, 0)
    assert error.type == SystemExit
    assert error.value.code == 1