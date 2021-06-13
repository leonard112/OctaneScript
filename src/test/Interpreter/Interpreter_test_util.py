# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import pytest
import mock
import builtins
import time
import threading
import _thread
from Interpreter import Interpreter


# References for timout class
# https://stackoverflow.com/questions/22454898/how-to-force-timeout-functions-in-python-windows-platform
# https://creativecommons.org/licenses/by-sa/2.5/
class timeout():
  def __init__(self, time):
    self.time= time
    self.exit=False

  def __enter__(self):
    threading.Thread(target=self.callme).start()

  def callme(self):
    time.sleep(self.time)
    if self.exit==False:
       _thread.interrupt_main()
  def __exit__(self, a, b, c):
       self.exit=True


@pytest.fixture(scope='function')
def interpreter(request):
    return Interpreter("test")


def assert_stack_trace(interpreter, script, line_numbers):
    try:
        interpreter.run_script(script, None)
    except:
        for line_number in line_numbers:
            assert interpreter.call_stack.pop().line_number + 1 == line_number

def assert_stack_trace_REPL(capfd, script, line_numbers):
    interpreter, console, failure = mock_REPL(capfd, script)
    for line_number in line_numbers:
        assert interpreter.call_stack.pop().line_number + 1 == line_number

def assert_code_works_in_REPL(capfd, script, expected_output):
        interpreter, console, failure = mock_REPL(capfd, script)
        assert console == expected_output

def assert_code_fails_in_REPL(capfd, script):
    try:
        with timeout(2):
            interpreter, console, failure = mock_REPL(capfd, script)
            if failure == True:
                raise Exception
    except:
        return
    pytest.fail()

def mock_REPL(capfd, script):
    interpreter = Interpreter("REPL")
    interpreter.exit_repl_on_error = True
    def input_side_effect():
        nonlocal script
        if (len(script) == 0):
            return "exit"
        line = script[0]
        script = script[1:]
        return line
    with mock.patch.object(builtins, 'input', lambda _: input_side_effect()):
        failure = False
        try:
            interpreter.run()
        except:
            failure = True
        console, err = capfd.readouterr()
        return interpreter, console, failure

def assert_error(interpreter, script):
    with pytest.raises(SystemExit) as error:
            interpreter.run_script(script, None)
    assert error.type == SystemExit
    assert error.value.code == 1

def assert_graceful_exit(interpreter, script):
    with pytest.raises(SystemExit) as error:
            interpreter.run_script(script, None)
    assert error.type == SystemExit
    assert error.value.code == 0

def assert_success(interpreter, script):
    try:
        interpreter.run_script(script, None)
    except:
        pytest.fail()