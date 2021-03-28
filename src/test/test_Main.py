# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

import pytest
from pytest_mock import mocker
from Main import *

def test_enters_repl_when_no_arguments_passed_in(mocker):
    mocked_enter_interpreter_as = mocker.patch('Main.enter_interpreter_as')
    perform_operation_based_on_arguments(['python'])
    mocked_enter_interpreter_as.assert_called_with("REPL")

def test_runs_octanescript_script_when_script_name_passed_in(mocker):
    mocked_enter_interpreter_as = mocker.patch('Main.enter_interpreter_as')
    perform_operation_based_on_arguments(['python', 'HelloWorld.os'])
    mocked_enter_interpreter_as.assert_called_with("HelloWorld.os")

def test_prints_info_when_info_flag_passed_in(mocker):
    mocked_print_info = mocker.patch('Main.print_info')
    perform_operation_based_on_arguments(['python', '--info'])
    mocked_print_info.assert_called()

def test_prints_info_when_i_flag_passed_in(mocker):
    mocked_print_info = mocker.patch('Main.print_info')
    perform_operation_based_on_arguments(['python', '-i'])
    mocked_print_info.assert_called()

def test_prints_version_when_version_flag_passed_in(mocker):
    mocked_print_version = mocker.patch('Main.print_version')
    perform_operation_based_on_arguments(['python', '--version'])
    mocked_print_version.assert_called()

def test_prints_version_when_v_flag_passed_in(mocker):
    mocked_print_version = mocker.patch('Main.print_version')
    perform_operation_based_on_arguments(['python', '-v'])
    mocked_print_version.assert_called()

def test_prints_license_when_license_flag_passed_in(mocker):
    mocked_print_license = mocker.patch('Main.print_license')
    perform_operation_based_on_arguments(['python', '--license'])
    mocked_print_license.assert_called()

def test_prints_license_when_l_flag_passed_in(mocker):
    mocked_print_license = mocker.patch('Main.print_license')
    perform_operation_based_on_arguments(['python', '-l'])
    mocked_print_license.assert_called()

def test_prints_help_info_when_help_flag_passed_in(mocker):
    mocked_print_help = mocker.patch('Main.print_help')
    perform_operation_based_on_arguments(['python', '--help'])
    mocked_print_help.assert_called()

def test_prints_help_info_when_h_flag_passed_in(mocker):
    mocked_print_help = mocker.patch('Main.print_help')
    perform_operation_based_on_arguments(['python', '-h'])
    mocked_print_help.assert_called()

def test_prints_help_info_when_invalid_argument_passed_in(mocker):
    mocked_print_help = mocker.patch('Main.print_help')
    perform_operation_based_on_arguments(['python', 'invalid'])
    mocked_print_help.assert_called()
