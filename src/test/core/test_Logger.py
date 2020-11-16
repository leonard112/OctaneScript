import pytest
from core.Line import Line
from core.Stack import Stack
from core.Logger import Logger

line = Line("TEST", 0, "test")
test_stack = Stack()
test_stack.push(line)

valid_log_functions = ["log", "logWarn", "logSuccess", "logError"]

def test_invalid_log_function_fails():
    assert_error(Logger("logInvlid", "'test'", test_stack, {}))
def test_valid_log_function_works():
    for log_function in valid_log_functions:
        assert_success(Logger(log_function, "'test'", test_stack, {}))


def assert_error(logger):
    with pytest.raises(SystemExit) as error:
            logger.log()
    assert error.type == SystemExit
    assert error.value.code == 1

def assert_success(logger):
    try:
        logger.log()
    except:
        pytest.fail()
