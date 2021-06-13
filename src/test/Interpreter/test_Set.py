# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from Interpreter_test_util import *
from Interpreter import Interpreter
from Reserved import reserved
import random


def test_valid_set_successful(interpreter):
    assert_success(interpreter, ["set x to 'value'"])


# ARRAYS
def test_set_can_set_array_values_to_the_results_of_function(interpreter):
    script = """
function returnZero()
    return 0
end
function returnOne()
    return 1
end
function returnTwo()
    return 2
end
set x to <returnZero(), returnOne(), returnTwo()>
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [0, 1, 2]

def test_fails_if_function_result_array_element_is_not_defined(interpreter):
    script = """
function returnZero()
    return 0
end
function returnOne()
    return 1
end
set x to <returnZero(), returnOne(), returnTwo()>
""".splitlines(True)
    assert_error(interpreter, script)

def test_set_can_set_array_values_to_the_results_of_a_functions_that_take_parameters(interpreter):
    script = """
function returnZero(paramOne, paramTwo)
    return 0
end
function returnOne(paramOne, paramTwo)
    return 1
end
function returnTwo(paramOne, paramTwo)
    return 2
end
set x to <returnZero(1, 2), returnOne("hello", "world"), returnTwo(True, False)>
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == [0, 1, 2]


# INPUT
def test_set_can_take_user_input(interpreter):
    with mock.patch.object(builtins, 'input', lambda _: "test"):
        assert_success(interpreter, ["set x to input"])
        assert interpreter.variables['x'] == "test"

def test_set_can_take_user_input_with_prompt(interpreter):
    with mock.patch.object(builtins, 'input', lambda _: "test"):
        assert_success(interpreter, ["set x to input 'Enter something: '"])
        assert interpreter.variables['x'] == "test"

def test_set_can_take_user_input_with_integer_prompt(interpreter):
    with mock.patch.object(builtins, 'input', lambda _: "test"):
        assert_success(interpreter, ["set x to input 1"])
        assert interpreter.variables['x'] == "test"

def test_set_can_take_user_input_with_decimal_prompt(interpreter):
    with mock.patch.object(builtins, 'input', lambda _: "test"):
        assert_success(interpreter, ["set x to input 1.1"])
        assert interpreter.variables['x'] == "test"

def test_set_can_take_user_input_with_boolean_prompt(interpreter):
    with mock.patch.object(builtins, 'input', lambda _: "test"):
        assert_success(interpreter, ["set x to input [true]"])
        assert interpreter.variables['x'] == "test"

def test_set_that_takes_user_input_fails_when_expression_passed_into_input_in_invalid(interpreter):
    with mock.patch.object(builtins, 'input', lambda _: "test"):
        assert_error(interpreter, ["set x to input invalid"])

def test_set_can_take_user_input_REPL(interpreter, capfd):
    script = """
set x to input
test
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "test\n\n")

def test_set_can_take_user_input_with_prompt_REPL(interpreter, capfd):
    script = """
set x to input 'Enter something'
test
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "test\n\n")

def test_set_can_take_user_input_with_integer_prompt_REPL(interpreter, capfd):
    script = """
set x to input 1
test
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "test\n\n")

def test_set_can_take_user_input_with_decimal_prompt_REPL(interpreter, capfd):
    script = """
set x to input 1.1
test
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "test\n\n")

def test_set_can_take_user_input_with_boolean_prompt_REPL(interpreter, capfd):
    script = """
set x to input true
test
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "test\n\n")

def test_set_that_takes_user_input_fails_when_expression_passed_into_input_in_invalid_REPL(interpreter, capfd):
    script = """
set x to input invalid
test
print x
""".splitlines(True)
    assert_code_fails_in_REPL(capfd, script)
    

# RANDOM DECIMAL
def test_set_can_take_a_random_decimal(interpreter):
    with mock.patch.object(random, 'random', lambda : 0.1):
        assert_success(interpreter, ["set x to randomDecimal"])
        assert interpreter.variables['x'] == 0.1

def test_set_can_take_a_random_decimal_REPL(interpreter, capfd):
    script = """
set x to randomDecimal
print x
""".splitlines(True)
    with mock.patch.object(random, 'random', lambda : 0.1):
        assert_code_works_in_REPL(capfd, script, "0.1\n")

def test_random_decimal_generation_fails_when_extra_parameters_are_passed_in(interpreter):
    assert_error(interpreter, ["set x to randomDecimal invalid"])

# RANDOM INTEGER
def test_set_can_take_a_random_integer_only_specifying_an_upper_limit(interpreter):
    with mock.patch.object(random, 'randint', lambda lower_limit, upper_limit: 5):
        assert_success(interpreter, ["set x to randomInteger 10"])
        assert interpreter.variables['x'] == 5

def test_set_can_take_a_random_integer_only_specifying_an_upper_limit_REPL(interpreter, capfd):
    script = """
set x to randomInteger 10
print x
""".splitlines(True)
    with mock.patch.object(random, 'randint', lambda lower_limit, upper_limit: 5):
        assert_code_works_in_REPL(capfd, script, "5\n")

def test_set_can_take_a_random_integer_only_specifying_an_upper_limit_as_the_result_of_a_function_call(interpreter):
    script = """
function returnTen()
    return 10
end
set x to randomInteger returnTen()
""".splitlines(True)
    with mock.patch.object(random, 'randint', lambda lower_limit, upper_limit: 5):
        assert_success(interpreter, script)
        assert interpreter.variables['x'] == 5

def test_set_random_integer_only_specifying_an_upper_limit_as_a_negative_number_fails(interpreter):
    assert_error(interpreter, ["set x to randomInteger -10"])

def test_set_random_integer_only_specifying_an_upper_limit_as_a_string_fails(interpreter):
    assert_error(interpreter, ["set x to randomInteger 'hello'"])

def test_set_random_integer_only_specifying_an_upper_limit_as_a_decimal_fails(interpreter):
    assert_error(interpreter, ["set x to randomInteger 1.1"])

def test_set_random_integer_only_specifying_an_upper_limit_as_a_boolean_fails(interpreter):
    assert_error(interpreter, ["set x to randomInteger [true]"])

def test_set_random_integer_only_specifying_an_upper_limit_as_an_invalid_value_fails(interpreter):
    assert_error(interpreter, ["set x to randomInteger invalid"])

def test_set_can_take_a_random_integer_with_a_lower_limit_and_an_upper_limit(interpreter):
    with mock.patch.object(random, 'randint', lambda lower_limit, upper_limit: 5):
        assert_success(interpreter, ["set x to randomInteger 0, 10"])
        assert interpreter.variables['x'] == 5

def test_set_can_take_a_random_integer_with_a_lower_limit_and_an_upper_limit_REPL(interpreter, capfd):
    script = """
set x to randomInteger 0, 10
print x
""".splitlines(True)
    with mock.patch.object(random, 'randint', lambda lower_limit, upper_limit: 5):
        assert_code_works_in_REPL(capfd, script, "5\n")

def test_set_can_take_a_random_integer_with_a_lower_limit_as_a_negative_number_and_an_upper_limit(interpreter):
    with mock.patch.object(random, 'randint', lambda lower_limit, upper_limit: 5):
        assert_success(interpreter, ["set x to randomInteger -10, 5"])
        assert interpreter.variables['x'] == 5

def test_set_can_take_a_random_integer_with_a_lower_limit_and_an_upper_limit_as_a_negative_number(interpreter):
    with mock.patch.object(random, 'randint', lambda lower_limit, upper_limit: 5):
        assert_success(interpreter, ["set x to randomInteger -10, -5"])
        assert interpreter.variables['x'] == 5

def test_set_can_take_a_random_integer_with_a_lower_limit_as_the_result_of_a_function_call_and_an_upper_limit(interpreter):
    script = """
function returnZero()
    return 0
end
set x to randomInteger returnZero(), 10
""".splitlines(True)
    with mock.patch.object(random, 'randint', lambda lower_limit, upper_limit: 5):
        assert_success(interpreter, script)
        assert interpreter.variables['x'] == 5

def test_set_can_take_a_random_integer_with_a_lower_limit_and_an_upper_limit_as_the_result_of_function_call(interpreter):
    script = """
function returnTen()
    return 10
end
set x to randomInteger 0, returnTen()
""".splitlines(True)
    with mock.patch.object(random, 'randint', lambda lower_limit, upper_limit: 5):
        assert_success(interpreter, script)
        assert interpreter.variables['x'] == 5

def test_set_random_integer_lower_limit_cannot_be_greater_than_upper_limit(interpreter):
    assert_error(interpreter, ["set x to randomInteger 10, 5"])

def test_set_random_integer_with_a_lower_limit_as_a_string_and_an_upper_limit(interpreter):
    assert_error(interpreter, ["set x to randomInteger 'hello', 10"])

def test_set_random_integer_with_a_lower_limit_as_a_decimal_and_an_upper_limit(interpreter):
    assert_error(interpreter, ["set x to randomInteger 1.1, 10"])

def test_set_random_integer_with_a_lower_limit_as_a_boolean_and_an_upper_limit(interpreter):
    assert_error(interpreter, ["set x to randomInteger [true], 10"])

def test_set_random_integer_with_a_lower_limit_as_an_invalid_value_and_an_upper_limit(interpreter):
    assert_error(interpreter, ["set x to randomInteger invalid, 10"])

def test_set_random_integer_with_a_lower_limit_and_an_upper_limit_as_a_string(interpreter):
    assert_error(interpreter, ["set x to randomInteger 0, 'hello'"])

def test_set_random_integer_with_a_lower_limit_and_an_upper_limit_as_a_decimal(interpreter):
    assert_error(interpreter, ["set x to randomInteger 0, 1.1"])

def test_set_random_integer_with_a_lower_limit_and_an_upper_limit_as_a_boolean(interpreter):
    assert_error(interpreter, ["set x to randomInteger 0, [true]"])

def test_set_random_integer_with_a_lower_limit_and_an_upper_limit_as_an_invalid_value(interpreter):
    assert_error(interpreter, ["set x to randomInteger 0, invalid"])

def test_set_random_integer_cannot_take_extra_parameters(interpreter):
    assert_error(interpreter, ["set x to randomInteger 0, 10, 12"])

def test_set_random_integer_cannot_have_a_comma_after_randomInteger(interpreter):
    assert_error(interpreter, ["set x to randomInteger, 10"])

def test_set_random_integer_cannot_have_extra_commas(interpreter):
    assert_error(interpreter, ["set x to randomInteger, 10,"])

def test_set_random_integer_cannot_take_zero_parameters(interpreter):
    assert_error(interpreter, ["set x to randomInteger"])