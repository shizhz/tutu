# -*- coding: utf-8 -*-
import unittest
from nose.tools import raises

from modules.command.cmd import validator
from modules.command.exceptions import InvalidParserParameterException, InvalidCommandException

@validator
def mock_is_valid_pass(ins, txt):
    return True

@validator
def mock_is_valid_not_pass(ins, txt):
    return False

@raises(InvalidParserParameterException)
def test_validator_no_parameter():
    mock_is_valid_pass()

@raises(InvalidParserParameterException)
def test_validator_one_parameter():
    mock_is_valid_pass(None)

@raises(InvalidParserParameterException)
def test_validator_invalid_parameter():
    mock_is_valid_pass(None, None)

def test_validator_pass():
    mock_is_valid_pass(None, "some string does not matter")

@raises(InvalidCommandException)
def test_validator_not_pass():
    mock_is_valid_not_pass(None, "some string does not matter")
