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
def test_valid_function_definition_constructs_function():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    assert b.function_variables == {'x' : None, 'y' : None, 'z' : None}
    assert b.function_start == 0
def test_function_can_be_defined_with_no_parameters():
    b = Function('testFunc()', [], test_stack, {}, {}, 0)
    assert b.function_variables == {}
    assert b.function_start == 0
def test_function_can_be_defined_with_no_parameters_and_extra_white_space():
    b = Function('testFunc(   )', [], test_stack, {}, {}, 0)
    assert b.function_variables == {}
    assert b.function_start == 0
def test_valid_function_definition_with_no_spaces_between_parameters_and_commas_works():
    b = Function('testFunc(x,y,z)', [], test_stack, {}, {}, 0)
    assert b.function_variables == {'x' : None, 'y' : None, 'z' : None}
    assert b.function_start == 0
def test_valid_function_definition_extra_spaces_between_parameters_and_commas_works():
    b = Function('testFunc(   x   ,   y   ,   z   )', [], test_stack, {}, {}, 0)
    assert b.function_variables == {'x' : None, 'y' : None, 'z' : None}
    assert b.function_start == 0
def test_extra_non_space_characters_after_function_defintion_raises_error():
    assert_error_on_init("testFunc (x, y, z) print 'test'")
def test_space_between_function_name_and_function_definition_raises_error():
    assert_error_on_init("testFunc (x, y, z)")
def test_passing_in_boolean_as_parameter_in_function_definition_raises_error():
    assert_error_on_init("testFunc(x, [true], z)")
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


# PARAMETER SUBSTITUION
def test_integers_can_be_passed_in_when_calling_function():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    b.populate_variables('(1, 2, 3)')
    assert b.function_variables == {'x' : 1, 'y' : 2, 'z' : 3}
def test_decimals_can_be_passed_in_when_calling_function():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    b.populate_variables('(1.1, 2.3, 3.4)')
    assert b.function_variables == {'x' : 1.1, 'y' : 2.3, 'z' : 3.4}
def test_double_quote_strings_can_be_passed_in_when_calling_function():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    b.populate_variables('("hello", "world", "test")')
    assert b.function_variables == {'x' : 'hello', 'y' : 'world', 'z' : 'test'}
def test_single_quote_strings_can_be_passed_in_when_calling_function():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    b.populate_variables("('hello', 'world', 'test')")
    assert b.function_variables == {'x' : 'hello', 'y' : 'world', 'z' : 'test'}
def test_boolean_values_can_be_passed_in_when_calling_function():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    b.populate_variables('(true, false, true)')
    assert b.function_variables == {'x' : True, 'y' : False, 'z' : True}
def test_variables_can_be_passed_in_when_calling_function():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {'a' : 1, 'b' : 2, 'c' : 3}, 0)
    b.populate_variables('(a, b, c)')
    assert b.function_variables == {'x' : 1, 'y' : 2, 'z' : 3}
def test_when_undefined_variables_are_passed_in_when_calling_function_error_raised():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    assert_error_on_populating_variables(b, "(a, b, c)")
def test_string_expressions_can_be_passed_in_when_calling_function():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    b.populate_variables('("hello" . 1, "world" . 2.3, "test" . "world")')
    assert b.function_variables == {'x' : 'hello1', 'y' : 'world2.3', 'z' : 'testworld'}
def test_math_expressions_can_be_passed_in_when_calling_function():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    b.populate_variables('((1+1), (2*(1+1)), (4/2))')
    assert b.function_variables == {'x' : 2, 'y' : 4, 'z' : 2}
def test_boolean_expressions_can_be_passed_in_when_calling_function():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    b.populate_variables('([true], ["hello" lessThan "world"], [true and false])')
    assert b.function_variables == {'x' : True, 'y' : True, 'z' : False}
def test_valid_parameter_subsitution_with_no_spaces_between_parameters_and_commas_when_calling_function_works():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    b.populate_variables('(1,2,3)')
    assert b.function_variables == {'x' : 1, 'y' : 2, 'z' : 3}
def test_valid_parameter_subsitution_with_extra_space_between_parameters_and_commas_when_calling_function_works():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    b.populate_variables('(   1  ,   2   ,   3   )')
    assert b.function_variables == {'x' : 1, 'y' : 2, 'z' : 3}
def test_passing_too_few_parameters_into_function_raises_error():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    assert_error_on_populating_variables(b, "(1, 2)")
def test_passing_too_many_parameters_into_function_raises_error():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    assert_error_on_populating_variables(b, "(1, 2, 3, 4)")
def test_passing_parameters_into_function_that_takes_no_parameters_raises_error():
    b = Function('testFunc()', [], test_stack, {}, {}, 0)
    assert_error_on_populating_variables(b, "(1)")
def test_passing_no_parameters_into_function_that_takes_no_parameters_works():
    b = Function('testFunc()', [], test_stack, {}, {}, 0)
    b.populate_variables('()')
    assert b.function_variables == {}
def test_passing_no_parameters_into_function_that_takes_no_parameters_with_white_space_works():
    b = Function('testFunc()', [], test_stack, {}, {}, 0)
    b.populate_variables('(   )')
    assert b.function_variables == {}
def test_extra_non_space_characters_after_right_parenthesis_raises_error():
    b = Function('testFunc(x, y, z)', [], test_stack, {}, {}, 0)
    assert_error_on_populating_variables(b, "(1, 2, 3) print 'test'")


def assert_error_on_init(function_definition):
    with pytest.raises(SystemExit) as error:
        Function(function_definition, [], test_stack, {}, {}, 0)
    assert error.type == SystemExit
    assert error.value.code == 1


def assert_error_on_populating_variables(function, parameters):
    with pytest.raises(SystemExit) as error:
        function.populate_variables(parameters)
    assert error.type == SystemExit
    assert error.value.code == 1