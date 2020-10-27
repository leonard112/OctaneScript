import sys
from Interpreter import Interpreter


def print_version():
    print(
"""
    Octane Version: 0.0.3 alpha
"""
)


def print_license():
    print(
"""
MIT License

Copyright (c) 2020 Leonard James Carcaramo Jr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    )


def print_help():   
    print(
"""
usage:
    script_name.octane   Run an Octane script."
    --version -v         Print Octane version info."
    --help -h            Get usage info.
"""
)


def perform_operation_based_on_arguments(arguments):
    if len(arguments) == 1:
        enter_interpreter_as("repl")
    elif arguments[1][-7:-6] == '.' and arguments[1][-6:] == 'octane' :
        enter_interpreter_as(arguments[1])
    elif arguments[1] == "--version" or arguments[1] == "-v":
        print_version()
    elif arguments[1] == "--license" or arguments[1] == "-l":
        print_license()
    elif arguments[1] == "--help" or arguments[1] == "-h":
        print_help()
    else :
        print_help()


def enter_interpreter_as(entrypoint):
    interpreter = Interpreter(entrypoint)
    interpreter.run()


if __name__ == '__main__':
    perform_operation_based_on_arguments(sys.argv)