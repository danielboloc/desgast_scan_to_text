#!/usr/bin/env python

"""Tests for `desgast_scan_to_text` package."""
import os
import pytest

from click.testing import CliRunner

from desgast_scan_to_text.azure_ai_vision import read_and_extract_page_ten

dir_path = os.path.dirname(os.path.realpath(__file__))
azure_page_10_test_1 = os.path.join(dir_path, "pg_0001.json")


def test_page_10_test_1():
    GRAL = read_and_extract_page_ten(azure_page_10_test_1)

    assert GRAL == {'N': 38, 'C16V-L': '83,3', 'C16V-B': '21,2', 'C13V-L': '83,8', 'C13V-B': '19,6', 'C23V-L': '86,0', 'C23V-B': '19,7', 'C26V-L': '81,9', 'C26V-B': '23,4', 'C16O-L': '66,6', 'C16O-B': '5,3', 'C26O-L': '71,3', 'C26O-B': '83', 'C16P-L': '77,4', 'C16P-B': '18,7', 'C13P-L': '79,4', 'C13P-B': '19,4', 'C23P-L': '75,7', 'C23P-B': '16,4', 'C26P-L': '68,8', 'C26P-B': '15,5', 'C46P-L': '84,7', 'C46P-B': '23,5', 'C43P-L': '85,1', 'C43P-B': '20,9', 'C33P-L': '82,9', 'C33P-B': '17,2', 'C36P-L': '79,0', 'C36P-B': '24,6', 'C46O-L': '66,5', 'C46O-B': '12,6', 'C36O-L': '66,7', 'C36O-B': '11,7', 'C46V-L': '76,3', 'C46V-B': '21,2', 'C43V-L': '69,2', 'C43V-B': '18,9', 'C33V-L': '66,0', 'C33V-B': '21,7', 'C36V-L': '76,7', 'C36V-B': '18,9'}
