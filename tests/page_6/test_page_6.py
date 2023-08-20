#!/usr/bin/env python

"""Tests for `desgast_scan_to_text` package."""
import os

from click.testing import CliRunner

from desgast_scan_to_text.azure_ai_vision import read_and_extract_page_six

dir_path = os.path.dirname(os.path.realpath(__file__))
azure_page_test_1 = os.path.join(dir_path, "pg_0001.json")
azure_page_test_2 = os.path.join(dir_path, "pg_0002.json")
azure_page_test_3 = os.path.join(dir_path, "pg_0003.json")
azure_page_test_4 = os.path.join(dir_path, "pg_0004.json")
azure_page_test_5 = os.path.join(dir_path, "pg_0005.json")



def test_page_test_1():
    test_1 = read_and_extract_page_six(azure_page_test_1)
    # mapped to quention numbers rather than the Q in excel (we will have to do it for the excel)
    assert test_1 == {'1': 4, '2': 4, '3': 0, '4': 2, '5': 2, '6': 2, '7': 2, '8': 0, '9': 0, '10': 4, '11': 2, '12': 4, '13': 4, '14': 0, '15': 3, '16': 0, '17': 0, '18': 4, '19': 3, '20': 3, '21': 0}

def test_page_test_2():
    test_2 = read_and_extract_page_six(azure_page_test_2)

    assert test_2 == {'1': 4, '2': 4, '3': 2, '4': 3, '5': 4, '6': 1, '8': 0, '9': 2, '10': 2, '11': 1, '12': 4, '13': 0, '14': 0, '15': 2, '16': 2, '17': 4, '18': 2, '19': 0, '20': 2, '21': 0}

def test_page_test_3():
    test_3 = read_and_extract_page_six(azure_page_test_3)

    assert test_3 == {'1': 0, '2': 3, '3': 0, '7': 0, '9': 1, '10': 2, '11': 2, '12': 2, '14': 0, '15': 2, '16': 0, '18': 0, '21': 0}

def test_page_test_4():
    test_4 = read_and_extract_page_six(azure_page_test_4)

    assert test_4 == {'1': 0, '2': 4, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 2, '13': 0, '14': 0, '15': 0, '16': 0, '17': 1, '18': 3, '19': 3, '20': 1, '21': 3}

def test_page_test_5():
    test_5 = read_and_extract_page_six(azure_page_test_5)

    assert test_5 == {'1': 3, '2': 2, '3': 2, '4': 2, '5': 2, '6': 3, '8': 3, '9': 0, '10': 0, '11': 2, '12': 0, '13': 2, '14': 0, '15': 2, '16': 0, '17': 1, '18': 3, '19': 1, '20': 2, '21': 0}