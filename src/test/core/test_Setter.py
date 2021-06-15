# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import pytest
import types
from core.Line import Line
from core.Stack import Stack
from core.Setter import Setter
from Reserved import reserved

line = Line("TEST", 0, "test")
test_stack = Stack()
test_stack.push(line)

def test_invalid_variable_name_fails():
    assert_error(Setter('&invlaid to "no good"', test_stack, {}, {}))
    assert_error(Setter('invlaid1 to "no good"', test_stack, {}, {}))
    assert_error(Setter('invla\'d to "no good"', test_stack, {}, {}))
def test_set_to_resserved_fails():
    for word in reserved:
        assert_error(Setter(word + ' to "no good"', test_stack, {}, {}))
def test_create_new_variable_successful():
    assert_success(Setter('x to "new value"', test_stack, {}, {}))
def test_overwrite_already_defined_successful():
    assert_success(Setter('x to "new value"', test_stack, {'x' : 'value'}, {}))

# NUMBERS AND MATH    
def test_stores_an_integer():
    set_number = Setter("x to 5", test_stack, {}, {})
    assert set_number.set()['x'] == 5
def test_stores_a_float():
    set_number = Setter("x to (3.33)", test_stack, {}, {})
    assert set_number.set()['x'] == 3.33
def test_stores_integer_result_of_math_operation():
    set_number = Setter("x to (2 * (1 + 1))", test_stack, {}, {})
    assert set_number.set()['x'] == 4
def test_stores_decimal_result_of_math_operation():
    set_number = Setter("x to ((1 / (2 + 2)) * 5)", test_stack, {}, {})
    assert set_number.set()['x'] == 1.25


# BOOLEANS
def test_stores_true_boolean():
    set_boolean = Setter("x to true", test_stack, {}, {})
    assert set_boolean.set()['x'] == True
def test_stores_false_boolean():
    set_boolean = Setter("x to false", test_stack, {}, {})
    assert set_boolean.set()['x'] == False
def test_stores_complex_true_result_of_boolean():
    set_boolean = Setter("x to [[15 equals (5 * 3)] and [\"hello\" notEquals \"world\"]]", test_stack, {}, {})
    assert set_boolean.set()['x'] == True
def test_stores_complex_false_result_of_boolean():
    set_boolean = Setter("x to [[15 notEquals (5 * 3)] and [\"hello\" notEquals \"world\"]]", test_stack, {}, {})
    assert set_boolean.set()['x'] == False


# ARRAYS
def test_stores_empty_array_when_using_the_array_keyword():
    set_array = Setter("x to array", test_stack, {}, {})
    assert set_array.set()['x'] == []
def test_stores_empty_array():
    set_array = Setter("x to <>", test_stack, {}, {})
    assert set_array.set()['x'] == []
def test_stores_array_with_only_one_non_boolean_element():
    set_array = Setter("x to <1>", test_stack, {}, {})
    assert set_array.set()['x'] == [1]
def test_stores_array_with_only_one_boolean_element():
    set_array = Setter("x to <true>", test_stack, {}, {})
    assert set_array.set()['x'] == [True]
def test_stores_an_array_of_numbers():
    set_array = Setter("x to <1, 2, 3>", test_stack, {}, {})
    assert set_array.set()['x'] == [1, 2, 3]
def test_stores_an_array_of_multiple_value_types():
    set_array = Setter("x to <1, 'hello world', true, <6,7>>", test_stack, {}, {})
    assert set_array.set()['x'] == [1, 'hello world', True, [6, 7]]


# ARRAY INDICIES AND SUBARRAYS
def test_stores_an_array_index():
    set_array_index = Setter("x to y<0>", test_stack, {'y': [1,2,3]}, {})
    assert set_array_index.set()['x'] == 1
def test_stores_a_subarray():
    set_array_index = Setter("x to y<0:2>", test_stack, {'y': [1,2,3]}, {})
    assert set_array_index.set()['x'] == [1,2]


# STRING INDICIES AND SUBSTRINGS
def test_stores_a_string_index():
    set_array_index = Setter("x to y<0>", test_stack, {'y': 'hello'}, {})
    assert set_array_index.set()['x'] == 'h'
def test_stores_a_substring():
    set_array_index = Setter("x to y<0:3>", test_stack, {'y': 'hello'}, {})
    assert set_array_index.set()['x'] == 'hel'


# TYPE
def test_stores_string_type():
    set_array_index = Setter("x to @Type:String", test_stack, {}, {})
    assert set_array_index.set()['x'] == str
def test_stores_string_type():
    set_array_index = Setter("x to @Type:Number", test_stack, {}, {})
    assert set_array_index.set()['x'] == float
def test_stores_string_type():
    set_array_index = Setter("x to @Type:Boolean", test_stack, {}, {})
    assert set_array_index.set()['x'] == bool
def test_stores_string_type():
    set_array_index = Setter("x to @Type:Array", test_stack, {}, {})
    assert set_array_index.set()['x'] == bool
def test_stores_string_type():
    set_array_index = Setter("x to @Type:Function", test_stack, {}, {})
    assert set_array_index.set()['x'] == types.FunctionType


# TYPE OF EXPRESSION
def test_stores_type_of_double_quote_string():
    set_array_index = Setter('x to type "hello"', test_stack, {}, {})
    assert set_array_index.set()['x'] == str
def test_stores_type_of_single_quote_string():
    set_array_index = Setter("x to type 'hello'", test_stack, {}, {})
    assert set_array_index.set()['x'] == str
def test_stores_type_of_integer():
    set_array_index = Setter("x to type 1", test_stack, {}, {})
    assert set_array_index.set()['x'] == int
def test_stores_type_of_decimal():
    set_array_index = Setter("x to type 1.1", test_stack, {}, {})
    assert set_array_index.set()['x'] == float
def test_stores_type_of_math():
    set_array_index = Setter("x to type (1 + 1)", test_stack, {}, {})
    assert set_array_index.set()['x'] == int
def test_stores_type_of_array():
    set_array_index = Setter("x to type <1, 2, 3>", test_stack, {}, {})
    assert set_array_index.set()['x'] == list


def assert_error(setter):
    with pytest.raises(SystemExit) as error:
            setter.set()
    assert error.type == SystemExit
    assert error.value.code == 1

def assert_success(setter):
    try:
        setter.set()
    except:
        pytest.fail()
