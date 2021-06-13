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
prepend "test" to extra x
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