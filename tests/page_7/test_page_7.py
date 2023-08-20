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

    assert test_1 == {'Q60': 2, 'Q61': 0, 'Q62': 4, 'Q63': 3, 'Q64': 4, 'Q65': 3, 'Q66': 3, 'Q67': 1, 'Q68': 4, 'Q69': 3, 'Q70': 1, 'Q71': 3, 'Q72': 4, 'Q73': 0}

def test_page_7_test_2():
    test_2 = read_and_extract_page_seven(azure_page_7_test_2)

    assert test_2 == {'Q60': 2, 'Q61': 4, 'Q62': 4, 'Q63': 1, 'Q64': 1, 'Q65': 2, 'Q66': 2, 'Q67': 3, 'Q68': 1, 'Q69': 0, 'Q70': 3, 'Q71': 4, 'Q72': 1}

def test_page_7_test_3():
    test_3 = read_and_extract_page_seven(azure_page_7_test_3)

    assert test_3 == {'Q60': 1, 'Q61': 1, 'Q62': 2, 'Q63': 2, 'Q64': 3}

def test_page_7_test_4():
    test_4 = read_and_extract_page_seven(azure_page_7_test_4)

    assert test_4 == {'Q60': 0, 'Q61': 0, 'Q62': 2, 'Q63': 3, 'Q64': 2, 'Q65': 2, 'Q66': 3, 'Q67': 0, 'Q68': 2, 'Q69': 2, 'Q70': 2, 'Q71': 2, 'Q72': 3, 'Q73': 1}

def test_page_7_test_5():
    test_5 = read_and_extract_page_seven(azure_page_7_test_5)

    assert test_5 == {'Q60': 4, 'Q61': 4, 'Q62': 4, 'Q63': 2, 'Q64': 2, 'Q65': 1, 'Q66': 2, 'Q67': 3, 'Q68': 2, 'Q69': 0, 'Q70': 3, 'Q71': 4, 'Q72': 2, 'Q73': 2}