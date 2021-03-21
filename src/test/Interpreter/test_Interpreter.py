# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from Interpreter_test_util import *
from Interpreter import Interpreter
from Reserved import reserved


def test_valid_print_functions_successful(interpreter):
    for i in range(0, 54, 1):
        assert_success(interpreter, [reserved[i] + " 'test'"])
def test_exit_successful(interpreter):
    assert_graceful_exit(interpreter, ["exit"])
def test_comment_and_blanks_ignored(interpreter):
    assert_success(interpreter, ["", "    ", "# This is a comment"])
def test_invalid_functions_fail(interpreter):
    assert_error(interpreter, ["invalid"])
    assert_error(interpreter, ["exitProgram"])
    assert_error(interpreter, ["setVal"])
def test_sleep_works_when_given_an_integer(interpreter):
    assert_success(interpreter, ["sleep 1"])
def test_sleep_works_when_given_zero(interpreter):
    assert_success(interpreter, ["sleep 0"])
def test_sleep_works_when_the_amount_of_seconds_to_sleep_for_is_the_result_of_a_function_call(interpreter):
    script = """
function returnOne()
    return 1
end
sleep returnOne()
""".splitlines(True)
    assert_success(interpreter, script)
def test_sleep_works_when_given_a_decimal(interpreter):
    assert_success(interpreter, ["sleep 1.1"])
def test_sleep_fails_when_given_a_string(interpreter):
    assert_error(interpreter, ["sleep 'hello'"])
def test_sleep_fails_when_given_a_boolean(interpreter):
    assert_error(interpreter, ["sleep [true]"])