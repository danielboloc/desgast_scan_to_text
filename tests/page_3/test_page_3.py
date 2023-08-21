#!/usr/bin/env python

"""Tests for `desgast_scan_to_text` package."""
import os

from click.testing import CliRunner

from desgast_scan_to_text.azure_ai_vision import read_and_extract_page_three

dir_path = os.path.dirname(os.path.realpath(__file__))
azure_page_test_1 = os.path.join(dir_path, "pg_0001.json")
azure_page_test_2 = os.path.join(dir_path, "pg_0002.json")
azure_page_test_3 = os.path.join(dir_path, "pg_0003.json")
azure_page_test_4 = os.path.join(dir_path, "pg_0004.json")
azure_page_test_5 = os.path.join(dir_path, "pg_0005.json")



def test_page_test_1():
    test_1 = read_and_extract_page_three(azure_page_test_1)
    assert test_1 == {'Q27': 'CANNOT_MAP_DATA', 'Q28': 'CANNOT_MAP_DATA', 'Q29': 'CANNOT_MAP_DATA', 'Q30': 'CANNOT_MAP_DATA', 'Q31': 'CANNOT_MAP_DATA', 'Q24': '2', 'Q25': '0,5', 'Q26': 0, 'conservador': 1, 'ortodontico': 1, 'quirurgico': 1, 'periodontal': 1, 'protesico': 0, 'Q23_posB': 4, 'Q23_posH': 1}

def test_page_test_2():
    test_2 = read_and_extract_page_three(azure_page_test_2)

    assert test_2 == {'Q27': 'CANNOT_MAP_DATA', 'Q28': 'CANNOT_MAP_DATA', 'Q29': 'CANNOT_MAP_DATA', 'Q30': 'CANNOT_MAP_DATA', 'Q31': 'CANNOT_MAP_DATA', 'Q24': 'A', 'Q25': 0, 'Q26': 2, 'conservador': 1, 'ortodontico': 1, 'quirurgico': 1, 'periodontal': 1, 'protesico': 0, 'Q23_posB': 4, 'Q23_posH': 4}

def test_page_test_3():
    test_3 = read_and_extract_page_three(azure_page_test_3)

    assert test_3 == {'Q27': 'CANNOT_MAP_DATA', 'Q28': 'CANNOT_MAP_DATA', 'Q29': 'CANNOT_MAP_DATA', 'Q30': 'CANNOT_MAP_DATA', 'Q31': 'CANNOT_MAP_DATA', 'ortodontico': 0, 'quirurgico': 0, 'periodontal': 0, 'Q23_posB': 1}

def test_page_test_4():
    test_4 = read_and_extract_page_three(azure_page_test_4)

    assert test_4 == {'Q27': 'CANNOT_MAP_DATA', 'Q28': 'CANNOT_MAP_DATA', 'Q29': 'CANNOT_MAP_DATA', 'Q30': 'CANNOT_MAP_DATA', 'Q31': 'CANNOT_MAP_DATA', 'Q24': 'Z', 'Q25': 0, 'conservador': 0, 'ortodontico': 0, 'quirurgico': 1, 'periodontal': 0, 'protesico': 1, 'Q23_posB': 4, 'Q23_posH': 4}

def test_page_test_5():
    test_5 = read_and_extract_page_three(azure_page_test_5)

    assert test_5 == {'Q27': 'CANNOT_MAP_DATA', 'Q28': 'CANNOT_MAP_DATA', 'Q29': 'CANNOT_MAP_DATA', 'Q30': 'CANNOT_MAP_DATA', 'Q31': 'CANNOT_MAP_DATA', 'Q24': '3', 'Q25': 0, 'Q26': 1, 'ortodontico': 1, 'quirurgico': 1, 'periodontal': 0, 'protesico': 1, 'Q23_posB': 1, 'Q23_posH': 1}