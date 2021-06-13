# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from Interpreter_test_util import *
from Interpreter import Interpreter


# NUMBER OF TIMES TO REPEAT
def test_repeat_can_loop_10_times(interpreter):
    script = """
set x to 0
repeat 10
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 10
def test_repeat_can_loop_10_times_REPL(capfd):
    script = """
set x to 0
repeat 10
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "10\n")

def test_repeat_works_when_run_fron_script_or_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 10
    set x to (x + 1)
end
invalid
""".splitlines(True)
    assert_stack_trace(interpreter, script, [6])
    assert_stack_trace_REPL(capfd, script, [6])

def test_repeat_gets_same_stack_trace_when_error_occurs_in_loop_from_script_or_REPL(capfd, interpreter):
    script = """
repeat 10
    print "This fails"
    invalid
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [4, 2])
    assert_stack_trace_REPL(capfd, script, [4, 2])

def test_repeat_can_loop_for_the_result_of_a_math_expression(interpreter):
    script = """
set x to 0
repeat (5 + 5)
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 10
def test_repeat_can_loop_for_the_result_of_a_math_expression_REPL(capfd):
    script = """
set x to 0
repeat (5 + 5)
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "10\n")

def test_repeat_can_loop_for_the_result_of_a_function_call(interpreter):
    script = """
function returnTen()
    return 10
end

set x to 0
repeat returnTen()
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 10
def test_repeat_can_loop_for_the_result_of_a_function_call_REPL(capfd):
    script = """
function returnTen()
    return 10
end

set x to 0
repeat returnTen()
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "10\n")

def test_amount_of_times_to_repeat_cannot_be_zero_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 0
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_amount_of_times_to_repeat_cannot_be_a_decimal_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 2.5
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_amount_of_times_to_repeat_cannot_be_a_string_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat "hello"
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_amount_of_times_to_repeat_cannot_be_a_boolean_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat [true]
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

# COUNTER
def test_repeat_can_have_counter_variable_that_auto_increments(interpreter):
    script = """
set x to 0
repeat 4, counter i
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 6
def test_repeat_can_have_counter_variable_that_auto_increments_REPL(capfd):
    script = """
set x to 0
repeat 4, counter i
    set x to (x + i)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "6\n")

def test_repeat_counter_variable_does_not_presist_after_repeat_finishes(interpreter):
    script = """
set x to 0
repeat 4, counter i
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    if 'i' in interpreter.variables:
        pytest.fail()
def test_repeat_counter_variable_does_not_presist_after_repeat_finishes_REPL(capfd):
    script = """
set x to 0
repeat 4, counter i
    set x to (x + i)
end
print i
""".splitlines(True)
    assert_code_fails_in_REPL(capfd, script)

def test_repeat_if_counter_overrides_existing_variable_it_will_be_restored_when_repeat_loop_is_done(interpreter):
    script = """
set i to "initial"
set x to 0
repeat 4, counter i
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['i'] == "initial"
def test_repeat_if_counter_overrides_existing_variable_it_will_be_restored_when_repeat_loop_is_done_REPL(capfd):
    script = """
set i to "initial"
set x to 0
repeat 4, counter i
    set x to (x + i)
end
print i
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "initial\n")

def test_repeat_counter_cannot_be_repeated_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 4, counter i, counter a
    set x to (x + i)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

# STEP
def test_repeat_can_have_a_step_specified(interpreter):
    script = """
set x to 0
repeat 10, step 2
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 5
def test_repeat_can_have_a_step_specified_REPL(capfd):
    script = """
set x to 0
repeat 10, step 2
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "5\n")

def test_repeat_step_cannot_be_zero_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 10, step 0
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_repeat_step_can_be_result_of_math_expression(interpreter):
    script = """
set x to 0
repeat 10, step (1 + 1)
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 5
def test_repeat_step_can_be_result_of_math_expression_REPL(capfd):
    script = """
set x to 0
repeat 10, step (1 + 1)
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "5\n")

def test_repeat_step_can_be_result_of_a_function_call(interpreter):
    script = """
function returnTwo()
    return 2
end
set x to 0
repeat 10, step returnTwo()
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 5
def test_repeat_step_can_be_result_of_a_function_call_REPL(capfd):
    script = """
function returnTwo()
    return 2
end
set x to 0
repeat 10, step returnTwo()
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "5\n")

def test_repeat_step_cannot_be_a_decimal_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 10, step 2.4
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_repeat_step_cannot_be_a_string_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 10, step "hello"
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_repeat_step_cannot_be_a_boolean_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 10, step [true]
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_repeat_step_can_only_be_defined_once_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 10, step 2, step 3
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

# START
def test_repeat_can_have_a_start_value(interpreter):
    script = """
set x to 0
repeat 5, start 2
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 3
def test_repeat_can_have_a_start_value_REPL(capfd):
    script = """
set x to 0
repeat 5, start 2
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "3\n")

def test_repeat_start_value_can_be_the_result_of_a_math_expression(interpreter):
    script = """
set x to 0
repeat 5, start (1 + 1)
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 3
def test_repeat_start_value_can_be_the_result_of_a_math_expression_REPL(capfd):
    script = """
set x to 0
repeat 5, start (1 + 1)
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "3\n")

def test_repeat_start_value_can_be_the_result_of_a_function_call(interpreter):
    script = """
function returnTwo()
    return 2
end
set x to 0
repeat 5, start returnTwo()
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 3
def test_repeat_start_value_can_be_the_result_of_a_function_call_REPL(capfd):
    script = """
function returnTwo()
    return 2
end
set x to 0
repeat 5, start returnTwo()
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "3\n")

def test_start_cannot_be_a_decimal_value_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 5, start 2.3
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_start_cannot_be_a_string_value_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 5, start "hello"
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_start_cannot_be_a_boolean_value_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 5, start [true]
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_start_can_only_be_defined_once_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 5, start 1, start 2
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

# COMBINATIONS OF EXTRA OPTIONS

def test_repeat_can_have_a_counter_and_a_step(interpreter):
    script = """
set x to 0
repeat 10, counter i, step 2
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 20
def test_repeat_can_have_a_counter_and_a_step_REPL(capfd):
    script = """
set x to 0
repeat 10, counter i, step 2
    set x to (x + i)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "20\n")

def test_repeat_can_have_a_counter_a_step_and_a_start(interpreter):
    script = """
set x to 0
repeat 10, counter i, step 2, start 4
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 18
def test_repeat_can_have_a_counter_a_step_and_a_start_REPL(capfd):
    script = """
set x to 0
repeat 10, counter i, step 2, start 4
    set x to (x + i)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "18\n")

def test_repeat_can_have_a_step_and_a_start(interpreter):
    script = """
set x to 0
repeat 10, step 2, start 4
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 3
def test_repeat_can_have_a_step_and_a_start_REPL(capfd):
    script = """
set x to 0
repeat 10, step 2, start 4
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "3\n")

def test_repeat_can_have_a_counter_and_a_start(interpreter):
    script = """
set x to 0
repeat 10, counter i, start 4
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 39
def test_repeat_can_have_a_counter_and_a_start_REPL(capfd):
    script = """
set x to 0
repeat 10, counter i, start 4
    set x to (x + i)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "39\n")

def test_repeat_counter_options_can_be_in_any_order(interpreter):
    script = """
set x to 0
repeat 10, counter i, start 4, step 2
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 18
def test_repeat_counter_options_can_be_in_any_order_REPL(capfd):
    script = """
set x to 0
repeat 10, counter i, start 4, step 2
    set x to (x + i)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "18\n")

def test_difference_between_repeat_and_start_cannot_be_positive_if_the_step_is_negative_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 10, start 0, step -1
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_difference_between_repeat_and_start_cannot_be_negative_if_the_step_is_positive_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat -10, start 0, step 1
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_difference_between_repeat_and_start_can_be_negative_if_the_step_is_negative(interpreter):
    script = """
set x to 0
repeat -10, start 0, step -2
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 5
def test_difference_between_repeat_and_start_can_be_negative_if_the_step_is_negative_REPL(capfd):
    script = """
set x to 0
repeat -10, start 0, step -2
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "5\n")


# OTHER TESTS
def test_code_continues_to_execute_after_repeat(interpreter):
    script = """
repeat 10
    set x to 1
end
set x to 3
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 3
def test_code_continues_to_execute_after_repeat_REPL(capfd):
    script = """
repeat 10
    set x to 1
end
set x to 3
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "3\n")

def test_repeat_and_counter_options_can_have_extra_white_space_between_them(interpreter):
    script = """
set x to 0
repeat  10  ,    counter  i ,   start   4    ,    step      2
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 18
def test_repeat_and_counter_options_can_have_extra_white_space_between_them_REPL(capfd):
    script = """
set x to 0
repeat  10  ,    counter  i ,   start   4    ,    step      2
    set x to (x + i)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "18\n")

def test_repeat_and_counter_options_must_have_commas_separating_them_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 10, counter i start 4, step 2
    set x to (x + i)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_repeat_cannot_take_an_invalid_option_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
repeat 10, invalid "value"
    set x to (x + i)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_repeat_lopps_can_be_rested(interpreter):
    script = """
set x to 0
repeat 10
    repeat 10
        set x to (x + 1)
    end
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 110
def test_repeat_loops_can_be_nested_REPL(capfd):
    script = """
set x to 0
repeat 10
    repeat 10
        set x to (x + 1)
    end
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "110\n")

def test_repeat_stack_trace_is_correct_for_script_and_REPL(capfd, interpreter):
    script = """
repeat 10
    print "This will fail."
    invalid
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [4, 2])
    assert_stack_trace_REPL(capfd, script, [4, 2])

def test_nested_repeat_stack_trace_is_correct_for_script_and_REPL(capfd, interpreter):
    script = """
repeat 10
    repeat 10
        print "This will fail."
        invalid
    end
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [5, 3, 2])
    assert_stack_trace_REPL(capfd, script, [5, 3, 2])

def test_repeat_stack_trace_is_correct_after_repeat_for_script_and_REPL(capfd, interpreter):
    script = """
repeat 10
    print "test."
end
invalid
""".splitlines(True)
    assert_stack_trace(interpreter, script, [5])
    assert_stack_trace_REPL(capfd, script, [5])