# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import pytest
import types
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
def test_arrays_can_be_concatenated_with_strings():
    assert Expression('"test". <1, 2, 3>', test_stack, {}).evaluate() == "test<1, 2, 3>"

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
        if word != "true" and word != "false" and word != "type":
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
def test_string_can_be_concatenated_to_array_variable():
    assert Expression('"test" . x', test_stack, {'x' : [1, 2, 3]}).evaluate() == "test<1, 2, 3>"
def test_string_can_be_concatenated_to_type_variable():
    assert Expression('"test" . x', test_stack, {'x' : str}).evaluate() == "test@Type:String"
def test_valid_complex_expression_successful():
    assert Expression(
        '"hello " . x . \' this expression is valid. Here is y \' . y', test_stack,
        {'x' : 'xValue', 'y' : 'yValue'}
    ).evaluate() == "hello xValue this expression is valid. Here is y yValue"


# ARRAY INITIALIZATION
def test_empty_array():
    assert Expression('<>', test_stack, {}).evaluate() == []
def test_empty_array_using_array_keyword():
    assert Expression('array', test_stack, {}).evaluate() == []
def test_array_with_one_element():
    assert Expression('<1>', test_stack, {}).evaluate() == [1]
def test_array_with_one_boolean_element():
    assert Expression('<true>', test_stack, {}).evaluate() == [True]
def test_array_of_double_quote_strings():
    assert Expression('<"hello", "world", "test">', test_stack, {}).evaluate() == ['hello', 'world', 'test']
def test_array_of_single_quote_strings():
    assert Expression("<'hello', 'world', 'test'>", test_stack, {}).evaluate() == ['hello', 'world', 'test']
def test_array_of_strings_expressions():
    assert Expression('<"hello" . "world", "test" . 0, "test" . 6>', test_stack, {}).evaluate() == ['helloworld', 'test0', 'test6']
def test_array_of_numbers():
    assert Expression('<1, 2, 3>', test_stack, {}).evaluate() == [1, 2, 3]
def test_array_can_have_extra_white_space():
    assert Expression('<  1   , 2 ,   3 >', test_stack, {}).evaluate() == [1, 2, 3]
def test_array_can_have_no_white_space():
    assert Expression('<1,2,3>', test_stack, {}).evaluate() == [1, 2, 3]
def test_array_of_math_expressions():
    assert Expression('<(1.5 + 2), (2*2), ((1+1)^2)>', test_stack, {}).evaluate() == [3.5, 4, 4]
def test_array_of_booleans():
    assert Expression('<true, false, true>', test_stack, {}).evaluate() == [True, False, True]
def test_array_of_boolean_expressions():
    assert Expression('<[1 equals 1], [1 notEquals 1], [2 greaterThan 1]>', test_stack, {}).evaluate() == [True, False, True]
def test_array_of_arrays():
    assert Expression('<<1,2>, <1,2,3>, <>>', test_stack, {}).evaluate() == [[1,2],[1,2,3],[]]
def test_array_with_a_lot_of_nested_arrays():
    assert Expression('<<1,2>, <1,2,<1,2,<1>>>, <>>', test_stack, {}).evaluate() == [[1,2],[1,2,[1,2,[1]]],[]]
def test_array_of_variables():
    assert Expression('<x, y, z>', test_stack, {'x': 1, 'y': 2, 'z': 3}).evaluate() == [1, 2, 3]
def test_array_of_array_elements():
    assert Expression('<x<0>, x<1>, x<2>>', test_stack, {'x': [1,2,3]}).evaluate() == [1, 2, 3]
def test_array_of_array_elements_with_extra_white_space():
    assert Expression('< x <  0 > , x  < 1   > , x  < 2   > >', test_stack, {'x': [1,2,3]}).evaluate() == [1, 2, 3]
    assert Expression('< x<  0 > , x< 1   > , x< 2   > >', test_stack, {'x': [1,2,3]}).evaluate() == [1, 2, 3]
def test_array_with_multiple_value_types():
    assert Expression('<1, "hello world", true, <6,7>, x>', test_stack, {'x': 5}).evaluate() == [1, "hello world", True, [6,7], 5]
def test_array_of_variables_fails_when_a_variable_is_undefined():
    assert_error(Expression('<x, y, z>', test_stack, {'x': 1, 'y': 2}))
def test_array_fails_when_start_angle_brackt_is_missing():
    assert_error(Expression('1, 2, 3>', test_stack, {}))
def test_array_fails_when_end_angle_brackt_is_missing():
    assert_error(Expression('<1, 2, 3', test_stack, {}))
def test_array_fails_when_start_and_end_angle_brackt_is_missing():
    assert_error(Expression('1, 2, 3', test_stack, {}))
def test_array_fails_when_a_comma_is_missing():
    assert_error(Expression('<1, 2 3>', test_stack, {}))
def test_array_fails_when_there_is_an_extra_comma_at_the_end():
    assert_error(Expression('<1, 2, 3,>', test_stack, {}))
def test_array_fails_when_there_is_an_extra_comma_at_the_beginning():
    assert_error(Expression('<,1, 2, 3>', test_stack, {}))
def test_array_fails_when_there_is_an_extra_comma_in_the_middle():
    assert_error(Expression('<,1, 2, 3>', test_stack, {}))
def test_array_fails_when_there_is_an_extra_comma_in_the_middle_of_complex_array():
    assert_error(Expression('<<1,2>, <1,2,<1,2,<1>>,>, <>>', test_stack, {}))
def test_array_fails_when_enclosed_in_parenthesis():
    assert_error(Expression('(1, 2, 3)', test_stack, {}))
def test_array_fails_when_enclosed_in_brackets():
    assert_error(Expression('[1, 2, 3]', test_stack, {}))


# ARRAY INDEX VALUES
def test_get_first_element_of_array():
    assert Expression('x<0>', test_stack, {'x': [1,2,3]}).evaluate() == 1
def test_get_array_element_can_contain_extra_white_space():
    assert Expression('x <  0   >', test_stack, {'x': [1,2,3]}).evaluate() == 1
    assert Expression('x<  0   >', test_stack, {'x': [1,2,3]}).evaluate() == 1
def test_get_first_element_of_array_using_first_keyword():
    assert Expression('x<first>', test_stack, {'x': [1,2,3]}).evaluate() == 1
def test_get_first_element_of_array_using_peek_keyword():
    assert Expression('x<peek>', test_stack, {'x': [1,2,3]}).evaluate() == 1
def test_get_last_element_of_array():
    assert Expression('x<2>', test_stack, {'x': [1,2,3]}).evaluate() == 3
def test_get_last_element_of_array_using_last_keyword():
    assert Expression('x<last>', test_stack, {'x': [1,2,3]}).evaluate() == 3
def test_get_element_from_middle_of_array():
    assert Expression('x<1>', test_stack, {'x': [1,2,3]}).evaluate() == 2
def test_get_element_from_middle_of_array_using_a_math_expression():
    assert Expression('x<(0+1)>', test_stack, {'x': [1,2,3]}).evaluate() == 2
def test_get_element_from_array_using_variable():
    assert Expression('x<index>', test_stack, {'x': [1,2,3], 'index': 1}).evaluate() == 2
def test_get_element_from_nested_array():
    assert Expression('x<0><1>', test_stack, {'x': [[1,4],2,3]}).evaluate() == 4
def test_get_element_from_nested_array_can_contain_extra_white_space():
    assert Expression('x <  0   > < 1   >', test_stack, {'x': [[1,4],2,3]}).evaluate() == 4
    assert Expression('x<  0   > < 1   >', test_stack, {'x': [[1,4],2,3]}).evaluate() == 4
def test_get_element_from_nested_array_using_a_math_expression():
    assert Expression('x<0><(0+1)>', test_stack, {'x': [[1,4],2,3]}).evaluate() == 4
def test_get_element_from_double_nested_array():
    assert Expression('x<0><1><2>', test_stack, {'x': [[1,[4,5,6]],2,3]}).evaluate() == 6
def test_get_element_from_array_will_fail_if_nested_array_element_does_not_exist():
    assert_error(Expression('x<0><1>', test_stack, {'x': [1,2,3]}))
def test_get_element_from_array_will_fail_if_nested_array_element_is_out_of_range():
    assert_error(Expression('x<0><5>', test_stack, {'x': [[1,2],2,3]}))
def test_get_element_from_array_will_fail_if_index_is_out_of_range():
    assert_error(Expression('x<5>', test_stack, {'x': [1,2,3]}))
def test_get_element_from_array_will_fail_if_index_is_negative():
    assert_error(Expression('x<-1>', test_stack, {'x': [1,2,3]}))
def test_get_element_from_array_will_fail_if_index_is_a_string():
    assert_error(Expression('x<"hello">', test_stack, {'x': [1,2,3]}))
def test_get_element_from_array_will_fail_if_index_is_a_string_expression():
    assert_error(Expression('x<"hello" . "world>', test_stack, {'x': [1,2,3]}))
def test_get_element_from_array_will_fail_if_index_is_a_decimal():
    assert_error(Expression('x<1.5>', test_stack, {'x': [1,2,3]}))
def test_get_element_from_array_will_fail_if_start_angle_bracket_is_missing():
    assert_error(Expression('x0>', test_stack, {'x': [1,2,3]}))
def test_get_element_from_array_will_fail_if_end_angle_bracket_is_missing():
    assert_error(Expression('x<0', test_stack, {'x': [1,2,3]}))
def test_get_element_from_array_will_fail_if_start_angle_bracket_is_missing_for_nested_array():
    assert_error(Expression('x<0>1>', test_stack, {'x': [[4,5],2,3]}))
def test_get_element_from_array_will_fail_if_end_angle_bracket_is_missing_for_nested_array():
    assert_error(Expression('x<0><1', test_stack, {'x': [[4,5],2,3]}))


# STRING INDEX VALUES
def test_get_first_element_of_string():
    assert Expression('x<0>', test_stack, {'x': 'hello'}).evaluate() == 'h'
def test_get_element_of_string_can_contain_white_space():
    assert Expression('x <  0   >', test_stack, {'x': 'hello'}).evaluate() == 'h'
    assert Expression('x<  0   >', test_stack, {'x': 'hello'}).evaluate() == 'h'
def test_get_first_element_of_string_using_first_keyword():
    assert Expression('x<first>', test_stack, {'x': 'hello'}).evaluate() == 'h'
def test_get_first_element_of_string_using_peek_keyword():
    assert Expression('x<peek>', test_stack, {'x': 'hello'}).evaluate() == 'h'
def test_get_last_element_of_string():
    assert Expression('x<4>', test_stack, {'x': 'hello'}).evaluate() == 'o'
def test_get_last_element_of_string_using_last_keyword():
    assert Expression('x<last>', test_stack, {'x': 'hello'}).evaluate() == 'o'
def test_get_element_from_middle_of_string():
    assert Expression('x<1>', test_stack, {'x': 'hello'}).evaluate() == 'e'
def test_get_element_from_middle_of_string_using_a_math_expression():
    assert Expression('x<(0+1)>', test_stack, {'x': 'hello'}).evaluate() == 'e'
def test_get_element_from_sting_using_variable():
    assert Expression('x<index>', test_stack, {'x': 'hello', 'index': 1}).evaluate() == 'e'
def test_cannot_get_nested_string_element_from_string():
    assert_error(Expression('x<0><1>', test_stack, {'x': 'hello'}))
def test_get_element_from_string_will_fail_if_index_is_out_of_range():
    assert_error(Expression('x<5>', test_stack, {'x': 'hello'}))
def test_get_element_from_string_will_fail_if_index_is_negative():
    assert_error(Expression('x<-1>', test_stack, {'x': 'hello'}))
def test_get_element_from_string_will_fail_if_index_is_a_string():
    assert_error(Expression('x<"hello">', test_stack, {'x': 'hello'}))
def test_get_element_from_string_will_fail_if_index_is_a_string_expression():
    assert_error(Expression('x<"hello" . "world">', test_stack, {'x': 'hello'}))
def test_get_element_from_string_will_fail_if_index_is_a_decimal():
    assert_error(Expression('x<1.5>', test_stack, {'x': 'hello'}))
def test_get_element_from_string_will_fail_if_start_angle_bracket_is_missing():
    assert_error(Expression('x0>', test_stack, {'x': 'hello'}))
def test_get_element_from_string_will_fail_if_end_angle_bracket_is_missing():
    assert_error(Expression('x<0', test_stack, {'x': 'hello'}))


# SUBARRAYS
def test_get_entire_array_as_subarray():
    assert Expression('x<0:3>', test_stack, {'x': [1,2,3]}).evaluate() == [1,2,3]
def test_get_subarray_can_contain_extra_whitespace():
    assert Expression('x <  0 :   3  >', test_stack, {'x': [1,2,3]}).evaluate() == [1,2,3]
    assert Expression('x<  0 :   3  >', test_stack, {'x': [1,2,3]}).evaluate() == [1,2,3]
def test_get_entire_array_as_subarray_using_start_and_end_keywords():
    assert Expression('x<start:end>', test_stack, {'x': [1,2,3]}).evaluate() == [1,2,3]
def test_get_first_half_of_array_as_subarray():
    assert Expression('x<0:2>', test_stack, {'x': [1,2,3]}).evaluate() == [1,2]
def test_get_first_half_of_array_as_subarray_using_start_keyword():
    assert Expression('x<start:2>', test_stack, {'x': [1,2,3]}).evaluate() == [1,2]
def test_get_last_half_of_array_as_subarray():
    assert Expression('x<1:3>', test_stack, {'x': [1,2,3]}).evaluate() == [2,3]
def test_get_last_half_of_array_as_subarray_using_end_keyword():
    assert Expression('x<1:end>', test_stack, {'x': [1,2,3]}).evaluate() == [2,3]
def test_get_subarray_of_nested_array_element():
    assert Expression('x<0><1:end>', test_stack, {'x': [[5,6,7],2,3]}).evaluate() == [6,7]
def test_get_subarray_of_subarray():
    assert Expression('x<0:4><1:end>', test_stack, {'x': [1,2,3,4,5]}).evaluate() == [2,3,4]
def test_subarray_can_take_variable_indicies():
    assert Expression('x<y:z>', test_stack, {'x': [1,2,3], 'y': 0, 'z': 2}).evaluate() == [1,2]
def test_subarray_using_math_expression_for_start_index():
    assert Expression('x<(1-1):2>', test_stack, {'x': [1,2,3]}).evaluate() == [1,2]
def test_subarray_using_math_expression_for_end_index():
    assert Expression('x<0:(1+1)>', test_stack, {'x': [1,2,3]}).evaluate() == [1,2]
def test_subarray_using_math_expression_indicies():
    assert Expression('x<(1-1):(1+1)>', test_stack, {'x': [1,2,3]}).evaluate() == [1,2]
def test_subarray_indicies_cannot_be_string_values():
    assert_error(Expression('x<"hello":2>', test_stack, {'x': [1,2,3]}))
def test_subarray_indicies_cannot_be_string_expressions():
    assert_error(Expression('x<"hello" . "world":2>', test_stack, {'x': [1,2,3]}))
def test_subarray_indicies_cannot_be_decimal_values():
    assert_error(Expression('x<1.5:2>', test_stack, {'x': [1,2,3]}))
def test_get_subarray_fails_when_start_index_is_negative():
    assert_error(Expression('x<-1:2>', test_stack, {'x': [1,2,3]}))
def test_get_subarray_fails_when_end_index_is_negative():
    assert_error(Expression('x<0:-1>', test_stack, {'x': [1,2,3]}))
def test_get_subarray_fails_when_start_index_is_greater_than_end_index():
    assert_error(Expression('x<2:0>', test_stack, {'x': [1,2,3]}))
def test_get_subarray_fails_when_start_index_is_out_of_range():
    assert_error(Expression('x<4:6>', test_stack, {'x': [1,2,3]}))
def test_get_subarray_fails_when_end_index_is_out_of_range():
    assert_error(Expression('x<0:4>', test_stack, {'x': [1,2,3]}))
def test_get_subarray_fails_when_start_angle_bracket_is_missing():
    assert_error(Expression('x0:2>', test_stack, {'x': [1,2,3]}))
def test_get_subarray_fails_when_end_angle_bracket_is_missing():
    assert_error(Expression('x<0:2', test_stack, {'x': [1,2,3]}))
def test_get_subarray_of_nested_array_element_fails_when_start_angle_bracket_is_missing():
    assert_error(Expression('x<0>1:end>', test_stack, {'x': [[5,6,7],2,3]}))
def test_get_subarray_of_nested_array_element_fails_when_end_angle_bracket_is_missing():
    assert_error(Expression('x<0><1:end', test_stack, {'x': [[5,6,7],2,3]}))


# SUBSTRINGS
def test_get_entire_string_as_substring():
    assert Expression('x<0:5>', test_stack, {'x': 'hello'}).evaluate() == 'hello'
def test_get_substring_can_contain_white_space():
    assert Expression('x <  0 :   5  >', test_stack, {'x': 'hello'}).evaluate() == 'hello'
    assert Expression('x<  0 :   5  >', test_stack, {'x': 'hello'}).evaluate() == 'hello'
def test_get_entire_string_as_substring_using_start_and_end_keywords():
    assert Expression('x<start:end>', test_stack, {'x': 'hello'}).evaluate() == 'hello'
def test_get_first_half_of_string_as_substring():
    assert Expression('x<0:3>', test_stack, {'x': 'hello'}).evaluate() == 'hel'
def test_get_first_half_of_string_as_substring_using_start_keyword():
    assert Expression('x<start:3>', test_stack, {'x': 'hello'}).evaluate() == 'hel'
def test_get_last_half_of_string_as_substring():
    assert Expression('x<3:5>', test_stack, {'x': 'hello'}).evaluate() == 'lo'
def test_get_last_half_of_string_as_substring_using_end_keyword():
    assert Expression('x<3:end>', test_stack, {'x': 'hello'}).evaluate() == 'lo'
def test_get_substring_of_string_element():
    assert Expression('x<0><start:end>', test_stack, {'x': 'hello'}).evaluate() == 'h'
def test_get_substring_of_string_array_element():
    assert Expression('x<0><3:end>', test_stack, {'x': ['hello',2,3]}).evaluate() == 'lo'
def test_get_substring_of_substring():
    assert Expression('x<0:4><1:end>', test_stack, {'x': 'hello'}).evaluate() == 'ell'
def test_substring_can_take_variable_indicies():
    assert Expression('x<y:z>', test_stack, {'x': 'hello', 'y': 0, 'z': 3}).evaluate() == 'hel'
def test_get_substring_using_math_expression_for_start_index():
    assert Expression('x<(1-1):3>', test_stack, {'x': 'hello'}).evaluate() == 'hel'
def test_get_substring_using_math_expression_for_end_index():
    assert Expression('x<0:(1+2)>', test_stack, {'x': 'hello'}).evaluate() == 'hel'
def test_get_substring_using_math_expression_indicies():
    assert Expression('x<(1-1):(1+2)>', test_stack, {'x': 'hello'}).evaluate() == 'hel'
def test_substring_indicies_cannot_be_string_values():
    assert_error(Expression('x<"hello":2>', test_stack, {'x': 'hello'}))
def test_substring_indicies_cannot_be_string_expressions():
    assert_error(Expression('x<"hello" . "world":2>', test_stack, {'x': 'hello'}))
def test_substring_indicies_cannot_be_decimal_values():
    assert_error(Expression('x<1.5:2>', test_stack, {'x': 'hello'}))
def test_get_substring_fails_when_start_index_is_negative():
    assert_error(Expression('x<-1:2>', test_stack, {'x': 'hello'}))
def test_get_substring_fails_when_end_index_is_negative():
    assert_error(Expression('x<0:-1>', test_stack, {'x': 'hello'}))
def test_get_substring_fails_when_end_index_is_greater_than_starte_index():
    assert_error(Expression('x<2:0>', test_stack, {'x': 'hello'}))
def test_get_substring_fails_when_start_index_is_out_of_range():
    assert_error(Expression('x<6:10>', test_stack, {'x': 'hello'}))
def test_get_substring_fails_when_end_index_is_out_of_range():
    assert_error(Expression('x<0:6>', test_stack, {'x': 'hello'}))
def test_get_substring_fails_when_start_angle_bracket_is_missing():
    assert_error(Expression('x0:2>', test_stack, {'x': 'hello'}))
def test_get_substing_fails_when_end_angle_bracket_is_missing():
    assert_error(Expression('x<0:2', test_stack, {'x': 'hello'}))
def test_get_substring_of_string_array_element_fails_when_start_angle_bracket_is_missing():
    assert_error(Expression('x<0>1:end>', test_stack, {'x': ['hello',2,3]}))
def test_get_substring_of_nested_string_array_element_fails_when_end_angle_bracket_is_missing():
    assert_error(Expression('x<0><1:end', test_stack, {'x': ['hello',2,3]}))


# TYPES
def test_get_string_type():
    assert Expression('@Type:String', test_stack, {}).evaluate() == str
def test_get_number_type():
    assert Expression('@Type:Number', test_stack, {}).evaluate() == float
def test_get_boolean_type():
    assert Expression('@Type:Boolean', test_stack, {}).evaluate() == bool
def test_get_array_type():
    assert Expression('@Type:Array', test_stack, {}).evaluate() == list
def test_get_array_function():
    assert Expression('@Type:Function', test_stack, {}).evaluate() == types.FunctionType


# TYPES OF VALUES
def test_get_type_of_string_value():
    assert Expression('type "hello"', test_stack, {}).evaluate() == str
def test_get_type_of_integer_value():
    assert Expression('type 1', test_stack, {}).evaluate() == int
def test_get_type_of_decimal_value():
    assert Expression('type 1.1', test_stack, {}).evaluate() == float
def test_get_type_of_boolean_value():
    assert Expression('type true', test_stack, {}).evaluate() == bool
def test_get_type_of_array_value():
    assert Expression('type <>', test_stack, {}).evaluate() == list


# TYPES OF EXPRESSIONS
def test_get_type_of_string_expression():
    assert Expression('type "hello" . 1 . "world"', test_stack, {}).evaluate() == str
def test_get_type_of_math_expression():
    assert Expression('type (1 + 2)', test_stack, {}).evaluate() == int
def test_get_type_of_boolean_expression():
    assert Expression('type [1 equals 1]', test_stack, {}).evaluate() == bool


# TYPES CONCATENATED WITH STRINGS
def test_get_string_type_can_be_concatenated_to_string():
    assert Expression('"hello" . @Type:String', test_stack, {}).evaluate() == "hello@Type:String"
def test_get_number_type_can_be_concatenated_to_string():
    assert Expression('"hello" . @Type:Number', test_stack, {}).evaluate() == "hello@Type:Number"
def test_get_boolean_type_can_be_concatenated_to_string():
    assert Expression('"hello" . @Type:Boolean', test_stack, {}).evaluate() == "hello@Type:Boolean"
def test_get_array_type_can_be_concatenated_to_string():
    assert Expression('"hello" . @Type:Array', test_stack, {}).evaluate() == "hello@Type:Array"
def test_get_function_type_can_be_concatenated_to_string():
    assert Expression('"hello" . @Type:Function', test_stack, {}).evaluate() == "hello@Type:Function"


# STRINGS CAN CONTAIN TYPES AND TYPES OF VALUES
def test_string_can_contain_type():
    assert Expression('"hello @Type:String"', test_stack, {}).evaluate() == "hello @Type:String"
    assert Expression('"hello type 1"', test_stack, {}).evaluate() == "hello type 1"


def assert_error(expression):
    with pytest.raises(SystemExit) as error:
            expression.evaluate()
    assert error.type == SystemExit
    assert error.value.code == 1