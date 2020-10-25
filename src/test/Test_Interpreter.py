import pytest
from core.Line import Line
from Interpreter import Interpreter
from Reserved import reserved

interpreter = Interpreter("test")

def test_valid_print_functions_successful():
    for i in range(0, 54, 1):
        assert_success(Line(reserved[i] + " 'test'", None, "TEST"))
def test_valid_set_successful():
    assert_success(Line("set x to 'value'", None, "TEST"))
def test_exit_successful():
    assert_graceful_exit(Line("exit", None, "TEST"))
def test_comment_and_blanks_ignored():
    assert_success(Line("", None, "TEST"))
    assert_success(Line("    ", None, "TEST"))
    assert_success(Line("# This is a comment", None, "TEST"))
def test_invalid_functions_fail():
    assert_error(Line("invalid", None, "TEST"))
    assert_error(Line("exitProgram", None, "TEST"))
    assert_error(Line("setVal", None, "TEST"))

def assert_error(line):
    with pytest.raises(SystemExit) as error:
            interpreter.execute(line)
    assert error.type == SystemExit
    assert error.value.code == 1

def assert_graceful_exit(line):
    with pytest.raises(SystemExit) as error:
            interpreter.execute(line)
    assert error.type == SystemExit
    assert error.value.code == 0

def assert_success(line):
    try:
        interpreter.execute(line)
    except:
        pytest.fail()