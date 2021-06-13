# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from Interpreter_test_util import *
from Interpreter import Interpreter


# FUNCTIONS DEFINITION
def test_function_can_be_defined(interpreter):
    script = """
function testFunc(x, y, z)
    print x
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.functions["testFunc"]
    assert interpreter.functions["testFunc"].function_start == 1

def test_function_fails_if_not_proceeded_by_end(interpreter):
    script = """
function testFunc(x, y, z)
    print x
""".splitlines(True)
    assert_error(interpreter, script)

def test_multiple_functions_can_be_defined(interpreter):
    script = """
function testFunc(x, y, z)
    print z
end
function testFunc2(x, y)
    print y
end
function testFunc3(x)
    print x
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.functions["testFunc"]
    assert interpreter.functions["testFunc"].function_start == 1
    assert interpreter.functions["testFunc2"]
    assert interpreter.functions["testFunc2"].function_start == 4
    assert interpreter.functions["testFunc3"]
    assert interpreter.functions["testFunc3"].function_start == 7

def test_function_cannot_be_defined_more_than_once(capfd, interpreter):
    script = """
function testFunc(x, y, z)
    print x
end
function testFunc(x, y)
    print y
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [5])
    assert_stack_trace_REPL(capfd, script, [5])

def test_function_cannot_have_the_same_name_as_a_defined_variable(capfd, interpreter):
    script = """
set test to "test"
function test(x, y, z)
    print x
end
""".splitlines(True)
    assert_stack_trace(interpreter, script, [3])
    assert_stack_trace_REPL(capfd, script, [3])

def test_variable_cannot_have_the_same_name_as_a_defined_function(capfd, interpreter):
    script = """
function test(x, y, z)
    print x
end
set test to "test"
""".splitlines(True)
    assert_stack_trace(interpreter, script, [5])
    assert_stack_trace_REPL(capfd, script, [5])

def test_function_can_be_called_and_executes_as_expected_after_being_defined(capfd, interpreter):
    script = """
function test(x, y, z)
    print x
    invalid
end
print "Entering function"
test(1, 2, 3)
""".splitlines(True)
    assert_stack_trace(interpreter, script, [4, 7])
    assert_stack_trace_REPL(capfd, script, [4, 7])

def test_code_after_function_call_continues_execution_where_it_left_off_after_function_finishes(capfd, interpreter):
    script = """
function test(x, y, z)
    print x
end
print "Entering function"
test(1, 2, 3)
print "Function finished"
invalid
""".splitlines(True)
    assert_stack_trace(interpreter, script, [8])
    assert_stack_trace_REPL(capfd, script, [8])

def test_function_can_be_called_from_another_function(capfd, interpreter):
    script = """
function test(x, y, z)
    test2(x)
end
function test2(x)
    print x
    invalid
end
print "Entering function"
test(1, 2, 3)
""".splitlines(True)
    assert_stack_trace(interpreter, script, [7, 3, 10])
    assert_stack_trace_REPL(capfd, script, [7, 3, 10])

def test_function_cannot_access_variables_that_are_out_of_scope(capfd, interpreter):
    script = """
set a to "global but not available to functions."
function test(x, y, z)
    print a
end
print "Entering function"
test(1, 2, 3)
""".splitlines(True)
    assert_stack_trace(interpreter, script, [4, 7])
    assert_stack_trace_REPL(capfd, script, [4, 7])

def test_variables_can_be_created_within_function_scope(capfd, interpreter):
    script = """
function test(x, y, z)
    set a to "local"
    print a
end
test(1, 2, 3)
print a
""".splitlines(True)
    assert_stack_trace(interpreter, script, [7])
    assert_stack_trace_REPL(capfd, script, [7])

def test_conditionals_work_inside_function(capfd, interpreter):
    script = """
function test(x, y, z)
    if [false]
        print "This wont execute"
    else
        if [true]
            invalid
        end
    end
end
print "Entering function"
test(1, 2, 3)
""".splitlines(True)
    assert_stack_trace(interpreter, script, [7, 6, 5, 12])
    assert_stack_trace_REPL(capfd, script, [7, 6, 5, 12])

def test_function_cannot_be_defined_inside_function(capfd, interpreter):
    script = """
function test(x, y, z)
    function test2(x, y)
        print x
    end
end
print "Entering function"
test(1, 2, 3)
""".splitlines(True)
    assert_stack_trace(interpreter, script, [3, 2])
    assert_stack_trace_REPL(capfd, script, [3, 2])

def test_function_cannot_be_defined_inside_conditional_inside_function(capfd, interpreter):
    script = """
function test(x, y, z)
    if [false]
        print "wont execute"
    else
        if [true]
            function test2(x, y)
                print x
            end
        end
    end
end
print "Entering function"
test(1, 2, 3)
""".splitlines(True)
    assert_stack_trace(interpreter, script, [7, 2])
    assert_stack_trace_REPL(capfd, script, [7, 2])

def test_function_calls_get_popped_of_stack(capfd, interpreter):
    script = """
function returnHello()
    return "hello"
end
function returnWorld()
    return "world"
end
returnHello()
returnWorld()
invalid
""".splitlines(True)
    assert_stack_trace(interpreter, script, [10])
    assert_stack_trace_REPL(capfd, script, [10])

def test_function_can_return_all_value_types(interpreter):
    script = """
function returnString()
    return "string"
end
function addOne(x)
    return (x + 1)
end
function addPointFive(x)
    return (x + .5)
end
function returnBool()
    return true
end
function returnArray()
    return <1,2,3>
end

set stringValue to returnString()
set integerValue to addOne(1)
set decimalValue to addPointFive(1)
set booleanValue to returnBool()
set arrayValue to returnArray()
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables['stringValue'] == "string"
    assert interpreter.variables['integerValue'] == 2
    assert interpreter.variables['decimalValue'] == 1.5
    assert interpreter.variables['booleanValue'] == True
    assert interpreter.variables['arrayValue'] == [1, 2, 3]

def test_any_return_value_of_function_can_be_concatenated_with_string(interpreter):
    script = """
function returnString()
    return "string"
end
function addOne(x)
    return (x + 1)
end
function addPointFive(x)
    return (x + .5)
end
function returnBool()
    return true
end
function returnArray()
    return <1,2,3>
end

set stringValue to "hello" . returnString() . "world"
set integerValue to "hello" . addOne(1) . "world"
set decimalValue to "hello" . addPointFive(1) . "world"
set booleanValue to "hello" . returnBool() . "world"
set arrayValue to "hello" . returnArray() . "world"
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables['stringValue'] == "hellostringworld"
    assert interpreter.variables['integerValue'] == "hello2world"
    assert interpreter.variables['decimalValue'] == "hello1.5world"
    assert interpreter.variables['booleanValue'] == "hellotrueworld"
    assert interpreter.variables['arrayValue'] == "hello<1, 2, 3>world"

def test_number_return_value_of_function_can_be_evaluated_in_math_expression(interpreter):
    script = """
function test(x)
    return (x + 1)
end
set returnValue to (1 + test(1))
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables['returnValue'] == 3

def test_number_return_value_of_function_can_be_evaluated_in_boolean_expression(interpreter):
    script = """
function returnBool()
    return true
end
set returnValue to [true and returnBool()]
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables['returnValue'] == True

def test_recursion_works_when_returning_calls_to_self(interpreter):
    script = """
function shortCircuit()
    return "hello"
    print err
end

shortCircuit()
""".splitlines(True)
    interpreter.run_script(script, None)

def test_recursion_works(interpreter):
    script = """
function countDown(x)
    if [x lessThanEquals 0]
        return x
    else
        countDown((x-1))
    end
end

set val to countDown(10)
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables['val'] == 0

def test_recursion_works_when_return_calls_to_self(interpreter):
    script = """
function countDown(x)
    if [x greaterThan 0]
        return countDown((x-1))
    end
    return x
end

set val to countDown(10)
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables['val'] == 0

def test_recursion_works_when_return_calls_to_self_and_base_case_in_else(interpreter):
    script = """
function countDown(x)
    if [x greaterThan 0]
        return countDown((x-1))
    else
        return x
    end
end

set val to countDown(10)
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables['val'] == 0

def test_recursion_works_when_return_calls_to_self_and_base_case_in_else_with_redundant_nesting(interpreter):
    script = """
function countDown(x)
    if [x greaterThan 0]
        return countDown((x-1))
    else
        if [false]
            return "won't execute"
        elseIf [true]
            return x
        else
            return "won't execute"
        end
    end
end

set val to countDown(10)
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables['val'] == 0

def test_conditional_state_in_function_doesnt_affect_conditional_state_outside_function(interpreter):
    script = """
function countDown(x)
    if [x greaterThan 0]
        return countDown((x-1))
    else
        return x
    end
end

if [false]
    set val to "first if"
else
    if [false]
        set val to "nested if"
    elseIf [true]
        set val to countDown(10)
    else
        set val to "nested else"
    end
end
""".splitlines(True)
    interpreter.run_script(script, None)
    assert interpreter.variables['val'] == 0