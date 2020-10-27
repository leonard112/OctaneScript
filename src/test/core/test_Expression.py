import pytest
from core.Expression import Expression
from Interpreter import reserved

# STRING EVALUATION
def test_no_quotes_fails():
    assert_error(Expression('test', "TEST", {}))
def test_no_leading_quote_fails():
    assert_error(Expression('test"', "TEST", {}))
def test_no_trailing_quote_fails():
    assert_error(Expression('"test', "TEST", {}))
def test_enclosed_in_double_quotes_successful():
    assert_success(Expression('"test"', "TEST", {}))
def test_enclosed_in_single_quotes_sucessful():
    assert_success(Expression("'test'", "TEST", {}))

# STRING CONCATENATION
def test_missing_dot_fails():
    assert_error(Expression('"test" "test"', "TEST", {}))
def test_bad_delimiter_fails():
    assert_error(Expression('"test" + "test"', "TEST", {}))
    assert_error(Expression('"test" x "test"', "TEST", {}))
def test_leading_dot_fails():
    assert_error(Expression('. "test" . "test"', "TEST", {}))
def test_trailing_dot_fails():
    assert_error(Expression('"test" . "test" .', "TEST", {}))
def test_valid_concatenation_successful():
    assert_success(Expression('"test" . "test"', "TEST", {}))
    assert_success(Expression('"test" . "test" . "test"', "TEST", {}))

# VARIABLES
def test_not_found_fails():
    assert_error(Expression('x', "TEST", {}))
def test_reserved_fails():
    for word in reserved:
        assert_error(Expression(word, "TEST", {}))
def test_existing_variable_successful():
    assert_success(Expression('"test" . x', "TEST", {'x' : 'value'}))
def test_valid_complex_expression_successful():
    assert_success(Expression(
        '"hello " . x . \' this expression is valid. Here is y \' . y', "TEST",
        {'x' : 'xValue', 'y' : 'yValue'}
    ))

def assert_error(expression):
    with pytest.raises(SystemExit) as error:
            expression.evaluate()
    assert error.type == SystemExit
    assert error.value.code == 1

def assert_success(expression):
    try:
        expression.evaluate()
    except:
        pytest.fail()
