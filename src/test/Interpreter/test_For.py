# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from Interpreter_test_util import *
from Interpreter import Interpreter

def test_for_works(interpreter):
    script = """
set arrayOne to <"hello", 1, true>
set arrayTwo to array 
for element in arrayOne
    append element to arrayTwo
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['arrayTwo'] == ['hello', 1, True]
def test_for_works_REPL(capfd):
    script = """
set arrayOne to <"hello", 1, true>
set arrayTwo to array 
for element in arrayOne
    append element to arrayTwo
end
print arrayTwo
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "<'hello', 1, true>\n")

def test_nested_for_works(interpreter):
    script = """
set arrayOne to <<"hello", "world">, <1, 2>, <true, false>>
set arrayTwo to array 
for nestedArray in arrayOne
    for element in nestedArray
        append element to arrayTwo
    end
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['arrayTwo'] == ['hello', 'world', 1, 2, True, False]
def test_nested_for_works_REPL(capfd):
    script = """
set arrayOne to <<"hello", "world">, <1, 2>, <true, false>>
set arrayTwo to array 
for nestedArray in arrayOne
    for element in nestedArray
        append element to arrayTwo
    end
end
print arrayTwo
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "<'hello', 'world', 1, 2, true, false>\n")

def test_code_runs_after_for(interpreter):
    script = """
set arrayOne to <"hello", 1, true>
set arrayTwo to array 
for element in arrayOne
    append element to arrayTwo
end
append 80 to arrayTwo
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['arrayTwo'] == ['hello', 1, True, 80]
def test_code_runs_after_for_REPL(capfd):
    script = """
set arrayOne to <"hello", 1, true>
set arrayTwo to array 
for element in arrayOne
    append element to arrayTwo
end
append 80 to arrayTwo
print arrayTwo
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "<'hello', 1, true, 80>\n")

def test_for_stack_trace_is_correct_for_script_and_REPL(capfd, interpreter):
    script = """
set arrayOne to <"hello", 1, true>
for element in arrayOne
    print "This fails"
    invalid
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [5, 3])
    assert_stack_trace_REPL(capfd, script, [5, 3])

def test_nested_for_stack_trace_is_correct_for_script_and_REPL(capfd, interpreter):
    script = """
set arrayOne to <<"hello", "world">, <1, 2>, <true, false>>
for nestedArray in arrayOne
    for element in nestedArray
        print "This fails"
        invalid
    end
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [6, 4, 3])
    assert_stack_trace_REPL(capfd, script, [6, 4, 3])

def test_stack_trace_is_correct_after_for_for_script_and_REPL(capfd, interpreter):
    script = """
set arrayOne to <"hello", 1, true>
for element in arrayOne
    print element
end
invalid
""".splitlines(True)
    assert_stack_trace(interpreter, script, [6])
    assert_stack_trace_REPL(capfd, script, [6])

def test_for_can_take_anonymous_array(interpreter):
    script = """
set arrayTwo to array
for element in <"hello", 1, true>
    append element to arrayTwo
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['arrayTwo'] == ['hello', 1, True]
def test_for_can_take_anonymous_array_REPL(capfd):
    script = """
set arrayTwo to array
for element in <"hello", 1, true>
    append element to arrayTwo
end
print arrayTwo
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "<'hello', 1, true>\n")

def test_for_can_take_result_of_function_call(interpreter):
    script = """
function returnArray()
    return <"hello", 1, true>
end
set arrayTwo to array
for element in returnArray()
    append element to arrayTwo
end
""".splitlines(True)
    assert_success(interpreter, script)
    assert interpreter.variables['arrayTwo'] == ['hello', 1, True]
def test_for_can_take_result_of_function_call_REPL(capfd):
    script = """
function returnArray()
    return <"hello", 1, true>
end
set arrayTwo to array
for element in returnArray()
    append element to arrayTwo
end
print arrayTwo
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, "<'hello', 1, true>\n")

def test_for_fails_if_the_in_keyword_is_missing_for_script_and_REPL(capfd, interpreter):
    script = """
set arrayOne to <"hello", 1, true>
for element arrayOne
    print element
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_for_fails_if_extraneus_argument_is_given_for_script_and_REPL(capfd, interpreter):
    script = """
set arrayOne to <"hello", 1, true>
for element in arrayOne extra
    print element
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_for_fails_if_array_element_argument_is_not_given_for_script_and_REPL(capfd, interpreter):
    script = """
set arrayOne to <"hello", 1, true>
for in arrayOne
    print element
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_for_fails_if_array_argument_is_not_given_for_script_and_REPL(capfd, interpreter):
    script = """
set arrayOne to <"hello", 1, true>
for element in
    print element
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_for_fails_if_no_arguments_are_given_for_script_and_REPL(capfd, interpreter):
    script = """
set arrayOne to <"hello", 1, true>
for
    print element
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_for_fails_if_an_integer_is_given_for_script_and_REPL(capfd, interpreter):
    script = """
set x to 5
for element in x
    print element
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_for_fails_if_a_string_is_given_for_script_and_REPL(capfd, interpreter):
    script = """
set x to "hello"
for element in x
    print element
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)

def test_for_fails_if_a_boolean_is_given_for_script_and_REPL(capfd, interpreter):
    script = """
set x to true
for element in x
    print element
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)