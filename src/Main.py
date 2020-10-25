import sys
from Interpreter import Interpreter

def print_version():
    print(
"""
    Octane Version: 0.0.2 alpha
"""
)

def print_help():   
    print(
"""
usage:
    script_name.o   Run an Octane script." +
    --version -v    Print Octane version info." +
    --help -h       Get usage info.
"""
)

def perform_operation_based_on_arguments(arguments):
    if len(arguments) == 1:
        enter_interpreter_as("repl")

    elif arguments[1][-2] == '.' and arguments[1][-1] == 'o' :
        enter_interpreter_as(arguments[1])

    elif arguments[1] == "--version" or arguments[1] == "-v":
        print_version()

    elif arguments[1] == "--help" or arguments[1] == "-h":
        print_help()

    else :
        print_help()

def enter_interpreter_as(entrypoint):
    interpreter = Interpreter(entrypoint)
    interpreter.run()

if __name__ == '__main__':
    perform_operation_based_on_arguments(sys.argv)