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

def test_repeat_can_loop_for_the_result_of_a_math_expression(interpreter):
    script = """
set x to 0
repeat (5 + 5)
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 10

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

def test_amount_of_times_to_repeat_cannot_be_a_decimal(interpreter):
    script = """
set x to 0
repeat 2.5
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

def test_amount_of_times_to_repeat_cannot_be_a_string(interpreter):
    script = """
set x to 0
repeat "hello"
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

def test_amount_of_times_to_repeat_cannot_be_a_boolean(interpreter):
    script = """
set x to 0
repeat [true]
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

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

def test_repeat_counter_cannot_be_repeated(interpreter):
    script = """
set x to 0
repeat 4, counter i, counter a
    set x to (x + i)
end
""".splitlines(True)
    assert_error(interpreter, script)

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

def test_repeat_step_can_be_result_of_math_expression(interpreter):
    script = """
set x to 0
repeat 10, step (1 + 1)
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 5

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

def test_repeat_step_cannot_be_a_decimal(interpreter):
    script = """
set x to 0
repeat 10, step 2.4
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

def test_repeat_step_cannot_be_a_string(interpreter):
    script = """
set x to 0
repeat 10, step "hello"
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

def test_repeat_step_cannot_be_a_boolean(interpreter):
    script = """
set x to 0
repeat 10, step [true]
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

def test_repeat_step_can_only_be_defined_once(interpreter):
    script = """
set x to 0
repeat 10, step 2, step 3
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

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

def test_repeat_start_value_can_be_the_result_of_a_math_expression(interpreter):
    script = """
set x to 0
repeat 5, start (1 + 1)
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 3

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

def test_start_cannot_be_a_decimal_value(interpreter):
    script = """
set x to 0
repeat 5, start 2.3
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

def test_start_cannot_be_a_string_value(interpreter):
    script = """
set x to 0
repeat 5, start "hello"
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

def test_start_cannot_be_a_boolean_value(interpreter):
    script = """
set x to 0
repeat 5, start [true]
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

def test_start_can_only_be_defined_once(interpreter):
    script = """
set x to 0
repeat 5, start 1, start 2
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)

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

def test_repeat_can_have_a_counter_a_step_and_a_start(interpreter):
    script = """
set x to 0
repeat 10, counter i, step 2, start 4
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 18

def test_repeat_can_have_a_step_and_a_start(interpreter):
    script = """
set x to 0
repeat 10, step 2, start 4
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 3

def test_repeat_can_have_a_counter_and_a_start(interpreter):
    script = """
set x to 0
repeat 10, counter i, start 4
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 39

def test_repeat_counter_options_can_be_in_any_order(interpreter):
    script = """
set x to 0
repeat 10, counter i, start 4, step 2
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 18

# REPEAT WHILE
def test_repeat_while_works(interpreter):
    script = """
set x to 0
repeat while [x lessThan 10]
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 10

def test_repeat_while_works_when_run_fron_script_or_REPL(capfd, interpreter):
    script = """
set x to 0
repeat while [x lessThan 10]
    set x to (x + 1)
end
invalid
""".splitlines(True)
    assert_stack_trace(interpreter, script, [6])
    assert_stack_trace_REPL(capfd, script, [6])

def test_repeat_while_can_take_the_result_of_a_fuction(interpreter):
    script = """
function isLessThanTen(value)
    if [value lessThan 10]
        return true
    else
        return false
    end
end
set x to 0
repeat while [isLessThanTen(x)]
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 10

def test_repeat_while_can_contain_extra_white_space(interpreter):
    script = """
set x to 0
repeat   while  [    x  lessThan   10    ]
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 10

# OTHER TESTS
def test_code_continues_to_execute_after_repeat(interpreter):
    script = """
repeat 10
    print "hello"
end
set x to 3
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 3

def test_repeat_and_counter_options_can_have_extra_white_space_between_them(interpreter):
    script = """
set x to 0
repeat  10  ,    counter  i ,   start   4    ,    step      2
    set x to (x + i)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 18

def test_repeat_and_counter_options_must_have_commas_separating_them(interpreter):
    script = """
set x to 0
repeat 10, counter i start 4, step 2
    set x to (x + i)
end
""".splitlines(True)
    assert_error(interpreter, script)

def test_repeat_cannot_take_an_invalid_option(interpreter):
    script = """
set x to 0
repeat 10, invalid "value"
    set x to (x + i)
end
""".splitlines(True)
    assert_error(interpreter, script)

