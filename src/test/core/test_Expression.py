import pytest
from core.Line import Line
from core.Stack import Stack
from core.Expression import Expression
from Interpreter import reserved

line = Line("TEST", 0, "test")
test_stack = Stack()
test_stack.push(line)

# STRING EVALUATION
def test_no_quotes_fails():
    assert_error(Expression('test', test_stack, {}))
def test_no_leading_quote_fails():
    assert_error(Expression('test"', test_stack, {}))
def test_no_trailing_quote_fails():
    assert_error(Expression('"test', test_stack, {}))
def test_enclosed_in_double_quotes_successful():
    assert_success(Expression('"test"', test_stack, {}))
def test_enclosed_in_single_quotes_sucessful():
    assert_success(Expression("'test'", test_stack, {}))

# STRING CONCATENATION
def test_missing_dot_fails():
    assert_error(Expression('"test" "test"', test_stack, {}))
def test_bad_delimiter_fails():
    assert_error(Expression('"test" + "test"', test_stack, {}))
    assert_error(Expression('"test" x "test"', test_stack, {}))
def test_leading_dot_fails():
    assert_error(Expression('. "test" . "test"', test_stack, {}))
def test_trailing_dot_fails():
    assert_error(Expression('"test" . "test" .', test_stack, {}))
def test_vaid_concatenation_successful():
    assert_success(Expression('"test" . "test"', test_stack, {}))
    assert_success(Expression('"test" . "test" . "test"', test_stack, {}))
def test_valid_concanenation_with_varying_white_space_successful():
    assert_success(Expression('"test"."test"."test"', test_stack, {}))
    assert_success(Expression('"test" ."test"    .    "test"', test_stack, {}))
def test_math_can_be_concatenated():
    assert_success(Expression('"test". (1 + 1)', test_stack, {}))
def test_numbers_can_be_concatenated():
    assert_success(Expression('"test". 5', test_stack, {}))

# NUMBERS
def test_integer_successful():
    assert_success(Expression('5', test_stack, {}))
def test_decimal_successful():
    assert_success(Expression('(3.33)', test_stack, {}))

# MATH
def test_bad_math_expression_fails():
    assert_error(Expression('1 + 1', test_stack, {}))
def test_valid_math_exptression_successful():
    assert_success(Expression('(1 + 1)', test_stack, {}))

# VARIABLES
def test_not_found_fails():
    assert_error(Expression('x', test_stack, {}))
def test_reserved_fails():
    for word in reserved:
        assert_error(Expression(word, test_stack, {}))
def test_existing_string_variable_successful():
    assert_success(Expression('x', test_stack, {'x' : 'value'}))
    assert_success(Expression('"test" . x', test_stack, {'x' : 'value'}))
def test_existing_integer_variable_successful():
    assert_success(Expression('x', test_stack, {'x' : 5}))
    assert_success(Expression('"test" . x', test_stack, {'x' : 5}))
def test_existing_float_variable_successful():
    assert_success(Expression('x', test_stack, {'x' : 5.5}))
    assert_success(Expression('"test" . x', test_stack, {'x' : 5.5}))
def test_valid_complex_expression_successful():
    assert_success(Expression(
        '"hello " . x . \' this expression is valid. Here is y \' . y', test_stack,
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
