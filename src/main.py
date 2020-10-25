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

if __name__ == '__main__':
    if len(sys.argv) == 1:
        interpreter = Interpreter("repl")
        interpreter.run()

    elif sys.argv[1][-2] == '.' and sys.argv[1][-1] == 'o' :
        interpreter = Interpreter(sys.argv[1])
        interpreter.run()

    elif sys.argv[1] == "--version" or sys.argv[1] == "-v":
        print_version()

    elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print_help()

    else :
        print_help()