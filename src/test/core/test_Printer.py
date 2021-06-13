# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import pytest
from core.Line import Line
from core.Stack import Stack
from core.Printer import Printer
from Reserved import reserved

line = Line("TEST", 0, "test")
test_stack = Stack()
test_stack.push(line)

# STRING
def test_invalid_print_fuction_fails():
    assert_error(Printer("printInvalid", "'test'", test_stack, {}))
def test_valid_print_function_works():
    for i in range(0, 54, 1):
        assert_success(Printer(reserved[i], "'test'", test_stack, {}))

# Concatenation
def test_print_concatenation_works():
    assert_success(Printer("print", "'test' . 'test'", test_stack, {}))

# NUMBERS
def test_print_integer_works():
    assert_success(Printer("print", "5", test_stack, {}))
def test_print_decimal_works():
    assert_success(Printer("print", "5.55", test_stack, {}))

# MATH
def test_print_math_integer_works():
    assert_success(Printer("print", "(1 + 1)", test_stack, {}))
def test_print_math_decimal_works():
    assert_success(Printer("print", "(3 / 2)", test_stack, {}))


# ARRAY
def test_print_array_works():
    assert_success(Printer("print", "<1, 2, 3>", test_stack, {}))


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
