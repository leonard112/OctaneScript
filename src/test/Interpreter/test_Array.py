# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from Interpreter_test_util import *
from Interpreter import Interpreter
from Reserved import reserved


# APPEND
def test_value_can_be_appended_to_array(interpreter):
    script = """
set x to <1, 2, 3>
append "test" to x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2, 3, "test"]

def test_value_can_be_appended_to_array_with_to(interpreter):
    script = """
set xto to <1, 2, 3>
append "test" to xto
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['xto'] == [1, 2, 3, "test"]

def test_value_can_be_appended_to_empty_array(interpreter):
    script = """
set x to <>
append "test" to x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == ["test"]

def test_value_can_not_be_appended_to_array_that_doesnt_exist(interpreter):
    script = """
append "test" to x
""".splitlines(True)
    assert_error(interpreter, script)

def test_value_can_not_be_appended_to_something_that_is_not_an_array(interpreter):
    script = """
set x to 1
append "test" to x
""".splitlines(True)
    assert_error(interpreter, script)

def test_append_will_fail_if_to_keyword_is_missing(interpreter):
    script = """
set x to <1, 2, 3>
append "test" x
""".splitlines(True)
    assert_error(interpreter, script)

def test_append_will_fail_if_given_too_many_arguments(interpreter):
    script = """
set x to <1, 2, 3>
append "test" to extra x
""".splitlines(True)
    assert_error(interpreter, script)


# PREPEND
def test_value_can_be_prepended_to_array(interpreter):
    script = """
set x to <1, 2, 3>
prepend "test" to x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == ["test", 1, 2, 3]

def test_value_can_be_prepended_to_array_with_to(interpreter):
    script = """
set xto to <1, 2, 3>
prepend "test" to xto
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['xto'] == ["test", 1, 2, 3]

def test_value_can_be_prepended_to_empty_array(interpreter):
    script = """
set x to <>
prepend "test" to x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == ["test"]

def test_value_can_not_be_prepended_to_array_that_doesnt_exist(interpreter):
    script = """
prepend "test" to x
""".splitlines(True)
    assert_error(interpreter, script)

def test_value_can_not_be_prepended_to_something_that_is_not_an_array(interpreter):
    script = """
set x to 1
prepend "test" to x
""".splitlines(True)
    assert_error(interpreter, script)

def test_prepend_will_fail_if_to_keyword_is_missing(interpreter):
    script = """
set x to <1, 2, 3>
prepend "test" x
""".splitlines(True)
    assert_error(interpreter, script)

def test_prepend_will_fail_if_given_too_many_arguments(interpreter):
    script = """
set x to <1, 2, 3>
prepend "test" to extra x
""".splitlines(True)
    assert_error(interpreter, script)


# PUSH
def test_value_can_be_pushed_to_array(interpreter):
    script = """
set x to <1, 2, 3>
push "test" to x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == ["test" ,1, 2, 3]

def test_value_can_be_pushed_to_array_with_to(interpreter):
    script = """
set xto to <1, 2, 3>
push "test" to xto
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['xto'] == ["test" ,1, 2, 3]

def test_value_can_be_pushed_to_empty_array(interpreter):
    script = """
set x to <>
push "test" to x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == ["test"]

def test_value_can_not_be_pushed_array_that_doesnt_exist(interpreter):
    script = """
push "test" to x
""".splitlines(True)
    assert_error(interpreter, script)

def test_value_can_not_be_pushed_to_something_that_is_not_an_array(interpreter):
    script = """
set x to 1
push "test" to x
""".splitlines(True)
    assert_error(interpreter, script)

def test_push_will_fail_if_to_keyword_is_missing(interpreter):
    script = """
set x to <1, 2, 3>
push "test" x
""".splitlines(True)
    assert_error(interpreter, script)

def test_prepend_will_fail_if_given_too_many_arguments(interpreter):
    script = """
set x to <1, 2, 3>
push "test" to extra x
""".splitlines(True)
    assert_error(interpreter, script)


# REMOVELAST
def test_last_element_can_be_removed_from_array(interpreter):
    script = """
set x to <1, 2, 3>
removeLast from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2]

def test_last_element_can_be_removed_from_array_with_from(interpreter):
    script = """
set xfrom to <1, 2, 3>
removeLast from xfrom
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['xfrom'] == [1, 2]

def test_last_element_can_not_be_removed_from_array_that_is_not_stored_in_a_variable(interpreter):
    script = """
removeLast from <1, 2, 3>
""".splitlines(True)
    assert_error(interpreter, script)

def test_last_element_can_not_be_removed_from_empty_array(interpreter):
    script = """
set x to <>
removeLast from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_last_element_can_not_be_removed_from_array_that_doesnt_exist(interpreter):
    script = """
removeLast from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_last_element_can_not_be_removed_from_something_that_is_not_an_array(interpreter):
    script = """
set x to 1
removeLast from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_last_will_fail_if_from_keyword_is_missing(interpreter):
    script = """
set x to <1, 2, 3>
removeLast x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_last_will_fail_if_given_extra_argument_after_from(interpreter):
    script = """
set x to <1, 2, 3>
removeLast from extra x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_last_will_fail_if_given_extra_argument_before_from(interpreter):
    script = """
set x to <1, 2, 3>
removeLast extra from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_last_will_fail_if_given_extra_argument_after_array(interpreter):
    script = """
set x to <1, 2, 3>
removeLast from x extra
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_last_will_fail_if_given_extra_from_keyword_before_array(interpreter):
    script = """
set x to <1, 2, 3>
removeLast from from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_last_will_fail_if_given_extra_from_keyword_after_array(interpreter):
    script = """
set x to <1, 2, 3>
removeLast from x from
""".splitlines(True)
    assert_error(interpreter, script)


# REMOVEFIRST
def test_first_element_can_be_removed_from_array(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [2, 3]

def test_first_element_can_be_removed_from_array_with_from(interpreter):
    script = """
set xfrom to <1, 2, 3>
removeFirst from xfrom
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['xfrom'] == [2, 3]

def test_first_element_can_not_be_removed_from_array_that_is_not_stored_in_a_variable(interpreter):
    script = """
removeFirst from <1, 2, 3>
""".splitlines(True)
    assert_error(interpreter, script)

def test_first_element_can_not_be_removed_from_empty_array(interpreter):
    script = """
set x to <>
removeFirst from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_first_element_can_not_be_removed_from_array_that_doesnt_exist(interpreter):
    script = """
removeFirst from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_first_element_can_not_be_removed_from_something_that_is_not_an_array(interpreter):
    script = """
set x to 1
removeFirst from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_first_will_fail_if_from_keyword_is_missing(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_first_will_fail_if_given_extra_argument_after_from(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst from extra x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_first_will_fail_if_given_extra_argument_before_from(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst extra from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_first_will_fail_if_given_extra_argument_after_array(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst from x extra
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_first_will_fail_if_given_extra_from_keyword_before_array(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst from from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_first_will_fail_if_given_extra_from_keyword_after_array(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst from x from
""".splitlines(True)
    assert_error(interpreter, script)


# POP
def test_element_can_be_popped_from_array(interpreter):
    script = """
set x to <1, 2, 3>
pop from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [2, 3]

def test_element_can_be_popped_from_array_with_from(interpreter):
    script = """
set xfrom to <1, 2, 3>
pop from xfrom
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['xfrom'] == [2, 3]

def test_element_can_not_be_popped_from_array_that_is_not_stored_in_a_variable(interpreter):
    script = """
pop from <1, 2, 3>
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_can_not_be_popped_from_empty_array(interpreter):
    script = """
set x to <>
pop from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_can_not_be_popped_from_array_that_doesnt_exist(interpreter):
    script = """
pop from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_can_not_be_popped_from_something_that_is_not_an_array(interpreter):
    script = """
set x to 1
pop from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_pop_will_fail_if_from_keyword_is_missing(interpreter):
    script = """
set x to <1, 2, 3>
pop x
""".splitlines(True)
    assert_error(interpreter, script)

def test_pop_will_fail_if_given_extra_arument_after_from(interpreter):
    script = """
set x to <1, 2, 3>
pop from extra x
""".splitlines(True)
    assert_error(interpreter, script)

def test_pop_will_fail_if_given_extra_arument_before_from(interpreter):
    script = """
set x to <1, 2, 3>
pop extra from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_pop_will_fail_if_given_extra_arument_after_array(interpreter):
    script = """
set x to <1, 2, 3>
pop from x extra
""".splitlines(True)
    assert_error(interpreter, script)

def test_pop_will_fail_if_given_extra_from_keyword_before_array(interpreter):
    script = """
set x to <1, 2, 3>
pop from from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_pop_will_fail_if_given_extra_from_keyword_after_array(interpreter):
    script = """
set x to <1, 2, 3>
pop from x from
""".splitlines(True)
    assert_error(interpreter, script)


# REMOVE
def test_element_can_be_removed_from_index_zero(interpreter):
    script = """
set x to <1, 2, 3>
remove 0 from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [2, 3]

def test_element_can_be_removed_from_index_one(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 3]

def test_element_can_be_removed_from_index_two(interpreter):
    script = """
set x to <1, 2, 3>
remove 2 from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2]

def test_element_being_removed_can_be_a_variable(interpreter):
    script = """
set x to <1, 2, 3>
set index to 2
remove index from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2]

def test_element_being_removed_can_be_a_variable_that_contains_from(interpreter):
    script = """
set x to <1, 2, 3>
set indexfrom to 2
remove indexfrom from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2]

def test_element_being_removed_can_be_the_result_of_a_function(interpreter):
    script = """
function returnIndex()
    return 2
end
set x to <1, 2, 3>
remove returnIndex() from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2]

def test_element_being_removed_can_be_an_array_index(interpreter):
    script = """
set y to <1, 2, 3>
set x to <1, 2, 3>
set index to 2
remove y<1> from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2]

def test_element_being_removed_can_be_a_math_expression(interpreter):
    script = """
set x to <1, 2, 3>
remove (1 + 1) from x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2]

def test_element_can_not_be_removed_from_array_that_is_not_stored_in_a_variable(interpreter):
    script = """
remove 1 from <1, 2, 3>
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_being_removed_can_not_be_out_of_range(interpreter):
    script = """
set x to <1, 2, 3>
remove 10 from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_being_removed_can_not_be_a_string(interpreter):
    script = """
set x to <1, 2, 3>
remove "hello" from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_being_removed_can_not_be_a_string_expression(interpreter):
    script = """
set x to <1, 2, 3>
remove "hello" . "world" from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_being_removed_can_not_be_a_decimal(interpreter):
    script = """
set x to <1, 2, 3>
remove 1.5 from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_being_removed_can_not_be_a_decimal_result_of_math_expression(interpreter):
    script = """
set x to <1, 2, 3>
remove (3 / 2) from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_being_removed_can_not_be_a_boolean(interpreter):
    script = """
set x to <1, 2, 3>
remove true from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_being_removed_can_not_be_a_boolean_expression(interpreter):
    script = """
set x to <1, 2, 3>
remove [true and false] from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_can_not_be_removed_from_empty_array(interpreter):
    script = """
set x to <>
remove 1 from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_can_not_be_removed_from_array_that_doesnt_exist(interpreter):
    script = """
remove 1 from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_can_not_be_removed_from_something_that_is_not_an_array(interpreter):
    script = """
set x to 1
remove 1 from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_will_fail_if_from_keyword_is_missing(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_will_fail_if_too_many_arguments_are_given_after_from(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 from extra x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_will_fail_if_too_many_arguments_are_given_after_array(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 from x extra
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_will_fail_if_too_many_arguments_are_given_before_from(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 extra from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_will_fail_if_given_extra_from_keyword_before_array(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 from from x
""".splitlines(True)
    assert_error(interpreter, script)

def test_remove_will_fail_if_given_extra_from_keyword_after_array(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 from x from
""".splitlines(True)
    assert_error(interpreter, script)


# INSERTING REMOVED VALUES INTO VARIABLES
def test_last_element_can_be_removed_from_array_and_stored_to_a_variable(interpreter):
    script = """
set x to <1, 2, 3>
removeLast from x into y
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['y'] == 3

def test_last_element_can_be_removed_from_array_and_stored_to_a_variable_that_contains_into(interpreter):
    script = """
set x to <1, 2, 3>
removeLast from x into yinto
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['yinto'] == 3

def test_last_element_can_be_removed_from_array_and_stored_to_a_variable_that_already_exists(interpreter):
    script = """
set x to <1, 2, 3>
set y to "hello"
removeLast from x into y
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['y'] == 3

def test_last_element_cannot_be_removed_from_array_and_stored_to_a_variable_is_already_defined_as_function(interpreter):
    script = """
function y()
    return true
end
set x to <1, 2, 3>
removeLast from x into y
""".splitlines(True)
    assert_error(interpreter, script)

def test_last_element_cannot_be_removed_from_array_and_stored_to_something_that_is_not_a_variable(interpreter):
    script = """
set x to <1, 2, 3>
removeLast from x into "hello"
""".splitlines(True)
    assert_error(interpreter, script)

def test_last_element_cannot_be_removed_from_array_and_stored_to_a_variable_with_extra_into_keyword(interpreter):
    script = """
set x to <1, 2, 3>
removeLast from x into y into
""".splitlines(True)
    assert_error(interpreter, script)

def test_first_element_can_be_removed_from_array_and_stored_to_a_variable(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst from x into y
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['y'] == 1

def test_first_element_can_be_removed_from_array_and_stored_to_a_variable_that_contain_into(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst from x into yinto
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['yinto'] == 1

def test_first_element_can_be_removed_from_array_and_stored_to_a_variable_that_already_exists(interpreter):
    script = """
set x to <1, 2, 3>
set y to "hello"
removeFirst from x into y
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['y'] == 1

def test_first_element_cannot_be_removed_from_array_and_stored_to_a_variable_that_is_already_defined_as_a_function(interpreter):
    script = """
function y()
    return true
end
set x to <1, 2, 3>
removeFirst from x into y
""".splitlines(True)
    assert_error(interpreter, script)

def test_first_element_cannot_be_removed_from_array_and_stored_to_something_that_is_not_a_variable(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst from x into "hello"
""".splitlines(True)
    assert_error(interpreter, script)

def test_first_element_cannot_be_removed_from_array_and_stored_to_a_variable_with_extra_into_keyword(interpreter):
    script = """
set x to <1, 2, 3>
removeFirst from x into y into
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_can_be_popped_from_array_and_stored_to_a_variable(interpreter):
    script = """
set x to <1, 2, 3>
pop from x into y
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['y'] == 1

def test_element_can_be_popped_from_array_and_stored_to_a_variable_that_contains_into(interpreter):
    script = """
set x to <1, 2, 3>
pop from x into yinto
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['yinto'] == 1

def test_element_can_be_popped_from_array_and_stored_to_a_variable_that_already_exists(interpreter):
    script = """
set x to <1, 2, 3>
set y to "hello"
pop from x into y
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['y'] == 1

def test_element_cannot_be_popped_from_array_and_stored_to_a_variable_that_is_already_defined_as_function(interpreter):
    script = """
function y()
    return true
end
set x to <1, 2, 3>
pop from x into y
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_cannot_be_popped_from_array_and_stored_to_something_that_is_not_a_variable(interpreter):
    script = """
set x to <1, 2, 3>
pop from x into "hello"
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_cannot_be_popped_from_array_and_stored_to_a_variable_with_extra_into_keyword(interpreter):
    script = """
set x to <1, 2, 3>
pop from x into y into
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_at_index_can_be_removed_from_array_and_stored_to_a_variable(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 from x into y
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['y'] == 2

def test_element_at_index_can_be_removed_from_array_and_stored_to_a_variable_that_contains_into(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 from x into yinto
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['yinto'] == 2

def test_element_at_index_can_be_removed_from_array_and_stored_to_a_variable_that_already_exists(interpreter):
    script = """
set x to <1, 2, 3>
set y to "hello"
remove 1 from x into y
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['y'] == 2

def test_element_at_index_cannot_be_removed_from_array_and_stored_to_a_variable_that_is_already_defined_as_function(interpreter):
    script = """
function y()
    return true
end
set x to <1, 2, 3>
remove 1 from x into y
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_at_index_cannot_be_removed_from_array_and_stored_to_something_that_is_not_a_variable(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 from x into "hello"
""".splitlines(True)
    assert_error(interpreter, script)

def test_element_at_index_cannot_be_removed_from_array_and_stored_to_variable_with_extra_into_keyword(interpreter):
    script = """
set x to <1, 2, 3>
remove 1 from x into y into
""".splitlines(True)
    assert_error(interpreter, script)


# MERGE
def test_two_arrays_can_be_merged(interpreter):
    script = """
set x to <1, 2, 3>
set y to <4, 5>
merge y into x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2, 3, 4, 5]

def test_anonymous_array_can_be_merged_into_another_array(interpreter):
    script = """
set x to <1, 2, 3>
merge <4, 5> into x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2, 3, 4, 5]

def test_array_returned_by_function_can_be_merged_into_another_array(interpreter):
    script = """
function returnArray()
    return <4, 5>
end
set x to <1, 2, 3>
merge returnArray() into x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2, 3, 4, 5]

def test_into_array_can_contain_into(interpreter):
    script = """
set xinto to <1, 2, 3>
merge <4, 5> into xinto
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['xinto'] == [1, 2, 3, 4, 5]

def test_string_cannot_be_merged_into_an_array(interpreter):
    script = """
set x to <1, 2, 3>
merge "hello" into x
""".splitlines(True)
    assert_error(interpreter, script)

def test_integer_cannot_be_merged_into_an_array(interpreter):
    script = """
set x to <1, 2, 3>
merge 1 into x
""".splitlines(True)
    assert_error(interpreter, script)

def test_decimal_cannot_be_merged_into_an_array(interpreter):
    script = """
set x to <1, 2, 3>
merge 1.1 into x
""".splitlines(True)
    assert_error(interpreter, script)

def test_math_cannot_be_merged_into_an_array(interpreter):
    script = """
set x to <1, 2, 3>
merge (1 + 1) into x
""".splitlines(True)
    assert_error(interpreter, script)

def test_boolean_cannot_be_merged_into_an_array(interpreter):
    script = """
set x to <1, 2, 3>
merge true into x
""".splitlines(True)
    assert_error(interpreter, script)

def test_into_array_cannot_be_anonymous(interpreter):
    script = """
merge <4, 5> into <1, 2, 3>
""".splitlines(True)
    assert_error(interpreter, script)

def test_into_array_cannot_be_a_string(interpreter):
    script = """
set x to "hello"
merge <4, 5> into x
""".splitlines(True)
    assert_error(interpreter, script)

def test_into_array_cannot_be_an_integer(interpreter):
    script = """
set x to 1
merge <4, 5> into x
""".splitlines(True)
    assert_error(interpreter, script)

def test_into_array_cannot_be_a_decimal(interpreter):
    script = """
set x to 1.1
merge <4, 5> into x
""".splitlines(True)
    assert_error(interpreter, script)

def test_into_array_cannot_be_a_boolean(interpreter):
    script = """
set x to true
merge <4, 5> into x
""".splitlines(True)
    assert_error(interpreter, script)

def test_into_array_cannot_contain_extra_into_keyword(interpreter):
    script = """
set x to true
merge <4, 5> into into x
""".splitlines(True)
    assert_error(interpreter, script)

def test_into_array_cannot_be_missing_into_keyword(interpreter):
    script = """
set x to true
merge <4, 5> x
""".splitlines(True)
    assert_error(interpreter, script)

def test_into_array_cannot_have_extra_arguments_at_end(interpreter):
    script = """
set x to true
merge <4, 5> into x extra
""".splitlines(True)
    assert_error(interpreter, script)

def test_into_array_cannot_have_extra_arguments_before_into(interpreter):
    script = """
set x to true
merge <4, 5> extra into x
""".splitlines(True)
    assert_error(interpreter, script)


# SORT
def test_array_can_be_sorted(interpreter):
    script = """
set x to <2, 3, 1>
sort x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [1, 2, 3]

def test_anonymous_array_cannot_be_sorted(interpreter):
    script = """
sort <2, 3, 1>
""".splitlines(True)
    assert_error(interpreter, script)

def test_anything_that_is_not_an_array_cannot_be_sorted(interpreter):
    script = """
set x to "hello"
sort x
""".splitlines(True)
    assert_error(interpreter, script)

def test_result_array_of_function__cannot_be_sorted(interpreter):
    script = """
function returnArray()
    return <2, 3, 1>
sort returnArray()
""".splitlines(True)
    assert_error(interpreter, script)


# SORT REVERSE
def test_array_can_be_sorted_in_reverse_order(interpreter):
    script = """
set x to <2, 3, 1>
sortReverse x
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [3, 2, 1]

def test_anonymous_array_cannot_be_sorted_in_reverse_order(interpreter):
    script = """
sortReverse <2, 3, 1>
""".splitlines(True)
    assert_error(interpreter, script)

def test_anything_that_is_not_an_array_cannot_be_sorted_in_reverse_order(interpreter):
    script = """
set x to "hello"
sortReverse x
""".splitlines(True)
    assert_error(interpreter, script)

def test_result_array_of_function__cannot_be_sorted_in_reverse_order(interpreter):
    script = """
function returnArray()
    return <2, 3, 1>
sortReverse returnArray()
""".splitlines(True)
    assert_error(interpreter, script)