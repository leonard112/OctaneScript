# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from Interpreter_test_util import *
from Interpreter import Interpreter

def test_while_works(interpreter):
    script = """
set x to 0
while [x lessThan 10]
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 10
def test_while_works_REPL(capfd):
    script = """
set x to 0
while [x lessThan 10]
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, '10\n')

def test_nested_while_works(interpreter):
    script = """
set x to 0
while [x lessThan 20]
    while [x lessThan 10]
        set x to (x + 1)
    end
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 20
def test_nested_while_works_REPL(capfd):
    script = """
set x to 0
while [x lessThan 20]
    while [x lessThan 10]
        set x to (x + 1)
    end
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, '20\n')

def test_while_produces_correct_stack_trace_when_error_occurs_after_while_from_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
while [x lessThan 10]
    set x to (x + 1)
end
invalid
""".splitlines(True)
    assert_stack_trace(interpreter, script, [6])
    assert_stack_trace_REPL(capfd, script, [6])

def test_while_gets_same_stack_trace_when_error_occurs_in_loop_from_script_and_REPL(capfd, interpreter):
    script = """
while [true]
    print "This fails"
    invalid
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [4, 2])
    assert_stack_trace_REPL(capfd, script, [4, 2])

def test_while_gets_same_stack_trace_when_error_occurs_in_nested_loop_from_script_and_REPL(capfd, interpreter):
    script = """
while [true]
    while [true]
        print "This fails"
        invalid
    end
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [5, 3, 2])
    assert_stack_trace_REPL(capfd, script, [5, 3, 2])

def test_while_can_take_the_result_of_a_fuction(interpreter):
    script = """
function isLessThanTen(value)
    if [value lessThan 10]
        return true
    else
        return false
    end
end
set x to 0
while [isLessThanTen(x)]
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 10
def test_while_can_take_the_result_of_a_fuction_REPL(capfd):
    script = """
function isLessThanTen(value)
    if [value lessThan 10]
        return true
    else
        return false
    end
end
set x to 0
while [isLessThanTen(x)]
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, '10\n')

def test_while_can_contain_extra_white_space(interpreter):
    script = """
set x to 0
while  [    x  lessThan   10    ]
    set x to (x + 1)
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 10
def test_while_can_contain_extra_white_space_REPL(capfd):
    script = """
set x to 0
while  [    x  lessThan   10    ]
    set x to (x + 1)
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, '10\n')

def test_code_runs_after_while(interpreter):
    script = """
set x to 0
while [x lessThan 10]
    set x to (x + 1)
end
set x to (x + 1)
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['x'] == 11
def test_code_runs_after_while_REPL(capfd):
    script = """
set x to 0
while [x lessThan 10]
    set x to (x + 1)
end
set x to (x + 1)
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, '11\n')

def test_while_fails_when_given_invalid_expression_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
while [x < 10]
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_while_fails_when_boolean_argument_is_missing_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
while
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_while_fails_when_given_extra_arguments_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 0
while [x < 10] extra
    set x to (x + 1)
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)