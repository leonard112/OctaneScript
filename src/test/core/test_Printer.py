import pytest
from core.Printer import Printer
from Reserved import reserved

# STRING
def test_invalid_print_fuction_fails():
    assert_error(Printer("printInvalid", "'test'", "TEST", {}))
def test_valid_print_function_works():
    for i in range(0, 54, 1):
        assert_success(Printer(reserved[i], "'test'", "TEST", {}))

# Concatenation
def test_print_concatenation_works():
    assert_success(Printer("print", "'test' . 'test'", "TEST", {}))

# NUMBERS
def test_print_integer_works():
    assert_success(Printer("print", "5", "TEST", {}))
def test_print_decimal_works():
    assert_success(Printer("print", "(5.55)", "TEST", {}))

# MATH
def test_print_math_integer_works():
    assert_success(Printer("print", "(1 + 1)", "TEST", {}))
def test_print_math_decimal_works():
    assert_success(Printer("print", "(3 / 2)", "TEST", {}))


def assert_error(printer):
    with pytest.raises(SystemExit) as error:
            printer.print()
    assert error.type == SystemExit
    assert error.value.code == 1

def assert_success(printer):
    try:
        printer.print()
    except:
        pytest.fail()
