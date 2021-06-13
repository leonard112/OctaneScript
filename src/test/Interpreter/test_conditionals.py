# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from Interpreter_test_util import *
from Interpreter import Interpreter


# IF ONLY 

def test_if_true_functional(interpreter):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed'
def test_if_true_functional_REPL(capfd):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed\n')


def test_if_false_functional(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Unchanged'
def test_if_false_functional_REPL(capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Unchanged\n')


# IF AND ELSE

def test_runs_else_when_if_false(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by else'
def test_runs_else_when_if_false_REPL(capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by else\n')


def test_does_not_runs_else_when_if_true(interpreter):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by if'
def test_does_not_runs_else_when_if_true_REPL(capfd):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by if\n')


# IF AND ELSEIF

def test_runs_true_elseif_when_if_false(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [true]
    set x to "Changed by elseIf"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by elseIf'
def test_runs_true_elseif_when_if_false_REPL(capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [true]
    set x to "Changed by elseIf"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by elseIf\n')


def test_skips_elseif_when_if_true(interpreter):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by if'
def test_skips_elseif__when_if_true_REPL(capfd):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by if\n')


# IF, ELSEIF, AND ELSE

def test_runs_true_elseif_when_if_false_and_not_else(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [true]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by elseIf'
def test_runs_true_elseif_when_if_false_and_not_else_REPL(capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [true]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by elseIf\n')


def test_runs_else_when_if_and_elseif_false(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by else'
def test_runs_else_when_if_and_elseif_false_REPL(capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by else\n')


def test_skips_elseif_and_else_when_if_true(interpreter):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by if'
def test_skips_elseif_and_else_when_if_true_REPL(capfd):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by elseIf"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by if\n')


# LONG IF CHAIN

def test_long_if_chain_works_properly(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by first elseIf"
elseIf [false]
    set x to "Changed by second elseIf"
elseIf [true]
    set x to "Changed by fourth elseIf"
elseIf [true]
    set x to "Changed by fourth elseIf"
else
    set x to "Changed by else"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by fourth elseIf'
def test_long_if_chain_works_properly_REPL(capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseIf [false]
    set x to "Changed by first elseIf"
elseIf [false]
    set x to "Changed by second elseIf"
elseIf [true]
    set x to "Changed by fourth elseIf"
elseIf [true]
    set x to "Changed by fourth elseIf"
else
    set x to "Changed by else"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by fourth elseIf\n')


# MULTIPLE LINES IN CONDITIONAL TO EXECUTE

def test_conditional_can_handle_multiple_lines_of_code(interpreter):
    script = """
set x to "Unchanged"
set y to "Unchanged"
set z to "Unchanged"
if [true]
    set x to "x"
    set y to "y"
    set z to "z"
else
    set x to "This should not execute"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'x'
    assert interpreter.variables["y"] == 'y'
    assert interpreter.variables["z"] == 'z'
def test_conditional_can_handle_multiple_lines_of_code_REPL(capfd):
    script = """
set x to "Unchanged"
set y to "Unchanged"
set z to "Unchanged"
if [true]
    set x to "x"
    set y to "y"
    set z to "z"
else
    set x to "This should not execute"
end
print x
print y
print z
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'x\ny\nz\n')


# NESTING

def test_nested_conditionals_work_properly(interpreter):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by initial if"
    if [true]
        set x to "Changed by first nested if"
    end
    if [false]
        set x to "Nothing should be changed here"
    else
        if [true]
            set x to "Changed by if in else on second if chain"
        elseIf [true]
            set x to "should not execute because if was true"
        end
    end
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed by if in else on second if chain'
def test_nested_conditionals_work_properly_REPL(capfd):
    script = """
set x to "Unchanged"
if [true]
    set x to "Changed by initial if"
    if [true]
        set x to "Changed by first nested if"
    end
    if [false]
        set x to "Nothing should be changed here"
    else
        if [true]
            set x to "Changed by if in else on second if chain"
        elseIf [true]
            set x to "should not execute because if was true"
        end
    end
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed by if in else on second if chain\n')


def test_when_all_ifs_are_false_no_else_or_elseif_will_execute(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by first if.
    if [false]
        set x to "Changed by second if."
    else
        set x to "Changed by else."
    end
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Unchanged'
def test_when_all_ifs_are_false_no_else_or_elseif_will_execute_REPL(capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by first if.
    if [false]
        set x to "Changed by second if."
    else
        set x to "Changed by else."
    end
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Unchanged\n')


# SPACING

def test_valid_code_works_regardless_of_extra_lines(interpreter):
    script = """


set x to "Unchanged"

if [true]

    if [false]

        set x to "This line should be skiped"

    elseIf [false]
        set x to  "This line should be skiped"


    else


        set x to "Changed"


    end



end


""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed'
def test_valid_code_works_regardless_of_extra_lines_REPL(capfd):
    script = """


set x to "Unchanged"

if [true]

    if [false]

        set x to "This line should be skiped"

    elseIf [false]
        set x to  "This line should be skiped"


    else


        set x to "Changed"


    end



end


print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed\n')


def test_valid_code_works_regardless_of_spacing(interpreter):
    script = """
set x to "Unchanged"

    if [true]
if [false]
        set x to "This line should be skiped"
            elseIf [false]
        set x to  "This line should be skiped"
else
                set x to "Changed"
end
            end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'Changed'
def test_valid_code_works_regardless_of_spacing_REPL(capfd):
    script = """
set x to "Unchanged"

    if [true]
if [false]
        set x to "This line should be skiped"
            elseIf [false]
        set x to  "This line should be skiped"
else
                set x to "Changed"
end
            end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'Changed\n')


# BAD CODE THAT DOES NOT GET EXECUTED WILL NOT CAUSE ERROR

def test_bad_code_that_does_not_execute_will_not_fail(interpreter):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseif [false]
    invalid
else
    set x to "All bad code has been skiped due to if being false"
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 'All bad code has been skiped due to if being false'
def test_bad_code_that_does_not_execute_will_not_fail_REPL(capfd):
    script = """
set x to "Unchanged"
if [false]
    set x to "Changed by if"
elseif [false]
    invalid
else
    set x to "All bad code has been skiped due to if being false"
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, 'All bad code has been skiped due to if being false\n')


# EXTRA OR MISSING END

def test_missing_end_fails_for_script_and_REPL(capfd, interpreter):
    script = """
if [true]
    print "This will cause error"
if [true]
    print "This code should not be reached"
end
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)


def test_extra_end_fails_for_script_and_REPL(capfd, interpreter):
    script = """
if [true]
    print "first if will execute"
end
if [true]
    print "second if will execute"
end
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)


# DANGLING ELSE AND ELSEIF

def test_dangling_else_fails_for_script_and_REPL(capfd, interpreter):
    script = """
else
    print "This should fail"
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)


def test_dangling_elseif_fails_for_script_and_REPL(capfd, interpreter):
    script = """
elseIf [true]
    print "This should fail"
else
    print "This should fail"
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)


def test_nested_dangling_else_fails_for_script_and_REPL(capfd, interpreter):
    script = """
if [true]
    else
        print "This should fail"
    end
end
print "Error will occur before this is reached."
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)


def test_nested_dangling_elseif_fails_for_script_and_REPL(capfd, interpreter):
    script = """
if [true]
    elseIf [true]
        print "This should fail"
    else
        print "This should fail"
    end
end
    print "Error will occur before this is reached."
""".splitlines(True)
    assert_error(interpreter, script)
    assert_code_fails_in_REPL(capfd, script)


# CALL STACK

def test_stack_trace_valid_for_single_line_for_script_and_REPL(capfd, interpreter):
    script = """print "err""".splitlines(True)
    assert_stack_trace(interpreter, script, [1])
    assert_stack_trace_REPL(capfd, script, [1])


def test_stack_trace_valid_for_multi_line_for_script_and_REPL(capfd, interpreter):
    script = """
# This is a comment
print "test"
print "err
print "This will not be executed"
""".splitlines(True)
    assert_stack_trace(interpreter, script, [4])
    assert_stack_trace_REPL(capfd, script, [4])


def test_stack_trace_valid_for_nesting_for_script_and_REPL(capfd, interpreter):
    script = """
print "Outside of if"
if [true]
    print "In first if"
    if [false]
        print "This wont print"
    else
        if [false]
            print "This won't print"
        elseIf [true]
            print "err
        else
            print "This wont print"
        end
    end
end
print "This won't print"
""".splitlines(True)
    assert_stack_trace(interpreter, script, [11, 10, 7, 3])
    assert_stack_trace_REPL(capfd, script, [11, 10, 7, 3])


def test_stack_trace_after_completion_of_if_for_script_and_REPL(capfd, interpreter):
    script = """
print "Outside of if"
if [true]
    print "Inside if"
end
if [true]
    print "err
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [7, 6])
    assert_stack_trace_REPL(capfd, script, [7, 6])

def test_stack_trace_when_function_inside_if_fails_for_script_and_REPL(capfd, interpreter):
    script = """
function fails()
    invalid
end
if [true]
    set x to fails()
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [3, 6, 5])
    assert_stack_trace_REPL(capfd, script, [3, 6, 5])


# FUNCTIONS

def test_functions_can_be_called_inside_if(interpreter):
    script = """
function returnOne()
    return 1
end
if [true]
    set x to returnOne()
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables["x"] == 1
def test_functions_can_be_called_inside_if_REPL(capfd):
    script = """
function returnOne()
    return 1
end
if [true]
    set x to returnOne()
end
print x
""".splitlines(True)
    assert_code_works_in_REPL(capfd, script, '1\n')

