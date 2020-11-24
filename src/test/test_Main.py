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

def test_prints_version_when_version_flag_passed_in(mocker):
    mocked_print_version = mocker.patch('Main.print_version')
    perform_operation_based_on_arguments(['python', '--version'])
    mocked_print_version.assert_called()

def test_prints_version_when_v_flag_passed_in(mocker):
    mocked_print_version = mocker.patch('Main.print_version')
    perform_operation_based_on_arguments(['python', '-v'])
    mocked_print_version.assert_called()

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
