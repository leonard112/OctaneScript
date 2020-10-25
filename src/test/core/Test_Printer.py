import pytest
from core.Printer import Printer
from Reserved import reserved

def test_invalid_print_fuction_fails():
    assert_error(Printer("printInvalid", "'test'", "TEST", {}))
def test_valid_print_function_works():
    for i in range(0, 54, 1):
        assert_success(Printer(reserved[i], "'test'", "TEST", {}))

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