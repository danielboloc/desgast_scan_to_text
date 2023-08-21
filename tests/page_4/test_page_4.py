#!/usr/bin/env python

"""Tests for `desgast_scan_to_text` package."""
import os

from click.testing import CliRunner

from desgast_scan_to_text.azure_ai_vision import read_and_extract_page_four

dir_path = os.path.dirname(os.path.realpath(__file__))
azure_page_test_1 = os.path.join(dir_path, "pg_0001.json")
azure_page_test_2 = os.path.join(dir_path, "pg_0002.json")
azure_page_test_3 = os.path.join(dir_path, "pg_0003.json")
azure_page_test_4 = os.path.join(dir_path, "pg_0004.json")
azure_page_test_5 = os.path.join(dir_path, "pg_0005.json")



def test_page_test_1():
    test_1 = read_and_extract_page_four(azure_page_test_1)
    # mapped to quention numbers rather than the Q in excel (we will have to do it for the excel)
    assert test_1 == {'Q32': 0, 'Q33': 1, 'Q34': 0, 'Q35': 0, 'Q36': 1, 'Q37': 2, 'Q38': 3}

def test_page_test_2():
    test_2 = read_and_extract_page_four(azure_page_test_2)

    assert test_2 == {'Q32': 0, 'Q33': 1, 'Q34': 0, 'Q35': 0, 'Q36': 0, 'Q37': 4, 'Q38': 4}

def test_page_test_3():
    test_3 = read_and_extract_page_four(azure_page_test_3)

    assert test_3 == {'Q32': 0, 'Q33': 0, 'Q34': 0, 'Q35': 0, 'Q36': 0, 'Q37': 1, 'Q38': 0}

def test_page_test_4():
    test_4 = read_and_extract_page_four(azure_page_test_4)

    assert test_4 == {'Q32': 0, 'Q33': 0, 'Q34': 2, 'Q35': 0, 'Q36': 0, 'Q37': 1, 'Q38': 0}

def test_page_test_5():
    test_5 = read_and_extract_page_four(azure_page_test_5)

    assert test_5 == {'Q32': 0, 'Q33': 0, 'Q34': 0, 'Q35': 0, 'Q36': 0, 'Q37': 1, 'Q38': 0}