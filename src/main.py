import sys
from interpreter import run

def print_version():
    print(
"""
    Octane Version: 0.0.1 alpha
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
        run("repl")

    elif sys.argv[1][-2] == '.' and sys.argv[1][-1] == 'o' :
        run(sys.argv[1])

    elif sys.argv[1] == "--version" or sys.argv[1] == "-v":
        print_version()

    elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print_help()

    else :
        print_help()