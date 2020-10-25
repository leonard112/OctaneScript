import pytest
from core.Setter import Setter
from Reserved import reserved

def test_invalid_variable_name_fails():
    assert_error(Setter('&invlaid to "no good"', "TEST", {}))
    assert_error(Setter('invlaid1 to "no good"', "TEST", {}))
    assert_error(Setter('invla\'d to "no good"', "TEST", {}))
def test_set_to_resserved_fails():
    for word in reserved:
        assert_error(Setter(word + ' to "no good"', "TEST", {}))
def test_create_new_variable_successful():
    assert_success(Setter('x to "new value"', "TEST", {}))
def test_overwrite_already_defined_successful():
    assert_success(Setter('x to "new value"', "TEST", {'x' : 'value'}))

def assert_error(setter):
    with pytest.raises(SystemExit) as error:
            setter.set()
    assert error.type == SystemExit
    assert error.value.code == 1

def assert_success(setter):
    try:
        setter.set()
    except:
        pytest.fail()
