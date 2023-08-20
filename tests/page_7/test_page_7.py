#!/usr/bin/env python

"""Tests for `desgast_scan_to_text` package."""
import os

from click.testing import CliRunner

from desgast_scan_to_text.azure_ai_vision import read_and_extract_page_seven

dir_path = os.path.dirname(os.path.realpath(__file__))
azure_page_7_test_1 = os.path.join(dir_path, "pg_0001.json")
azure_page_7_test_2 = os.path.join(dir_path, "pg_0002.json")
azure_page_7_test_3 = os.path.join(dir_path, "pg_0003.json")
azure_page_7_test_4 = os.path.join(dir_path, "pg_0004.json")
azure_page_7_test_5 = os.path.join(dir_path, "pg_0005.json")



def test_page_7_test_1():
    test_1 = read_and_extract_page_seven(azure_page_7_test_1)

    # mapped to quention numbers rather than the Q in excel (we will have to do it for the excel)
    assert test_1 == {'1': 2, '2': 0, '3': 4, '4': 3, '5': 4, '6': 3, '7': 3, '8': 1, '9': 4, '10': 3, '11': 1, '12': 3, '13': 4, '14': 0}

def test_page_7_test_2():
    test_2 = read_and_extract_page_seven(azure_page_7_test_2)

    assert test_2 == {'1': 2, '2': 4, '3': 4, '4': 1, '5': 1, '6': 2, '7': 2, '8': 3, '9': 1, '10': 0, '11': 3, '12': 4, '13': 1}

def test_page_7_test_3():
    test_3 = read_and_extract_page_seven(azure_page_7_test_3)

    assert test_3 == {'3': 1, '5': 1, '7': 2, '10': 2, '12': 3}

def test_page_7_test_4():
    test_4 = read_and_extract_page_seven(azure_page_7_test_4)

    assert test_4 == {'1': 0, '2': 0, '3': 2, '4': 3, '5': 2, '6': 2, '7': 3, '8': 0, '9': 2, '10': 2, '11': 2, '12': 2, '13': 3, '14': 1}

def test_page_7_test_5():
    test_5 = read_and_extract_page_seven(azure_page_7_test_5)

    assert test_5 == {'1': 4, '2': 4, '3': 4, '4': 2, '5': 2, '6': 1, '7': 2, '8': 3, '9': 2, '10': 0, '11': 3, '12': 4, '13': 2, '14': 2}