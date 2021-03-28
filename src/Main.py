# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import sys
import platform
from Interpreter import Interpreter

name = "OctaneScript"
version = "Alpha DEV"
file_extension = ".os"
maintainer = "lcarcaramo@gmail.com"
project_home = "https://github.com/leonard112/OctaneScript"

def print_info():
    print(
"""========================================================================================
    %s Version: %s
    Arch: %s
    OS: %s %s
    License: MIT
    Maintainer: %s
    Maintained at: %s
========================================================================================"""
% (name, version, platform.machine(), platform.system(), platform.version(), maintainer, project_home))

def print_version():
    print("\n%s Version: %s\n" % (name, version))

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
    <no arguments>       Open REPL
    script_name%s       Run an %s program.
    --version -v         Print %s version information.
    --info -i            Print information about your %s installation.
    --license -l         Show license information.
    --help -h            Get usage information.
""" % (file_extension, name, name, name)
)


def perform_operation_based_on_arguments(arguments):
    if len(arguments) == 1:
        print_info()
        enter_interpreter_as("REPL")
    elif arguments[1][-3:] == file_extension :
        enter_interpreter_as(arguments[1])
    elif arguments[1] == "--version" or arguments[1] == "-v":
        print_version()
    elif arguments[1] == "--info" or arguments[1] == "-i":
        print_info()
    elif arguments[1] == "--license" or arguments[1] == "-l":
        print_license()
    elif arguments[1] == "--help" or arguments[1] == "-h":
        print_help()
    else :
        print_help()


def enter_interpreter_as(entrypoint):
    sys.setrecursionlimit(10**6)
    interpreter = Interpreter(entrypoint)
    interpreter.run()


if __name__ == '__main__':
    perform_operation_based_on_arguments(sys.argv)
