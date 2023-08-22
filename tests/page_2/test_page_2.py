#!/usr/bin/env python

"""Tests for `desgast_scan_to_text` package."""
import os

from click.testing import CliRunner

from desgast_scan_to_text.azure_ai_vision import read_and_extract_page_two

dir_path = os.path.dirname(os.path.realpath(__file__))
azure_page_test_1 = os.path.join(dir_path, "pg_0001.json")
azure_page_test_2 = os.path.join(dir_path, "pg_0002.json")
azure_page_test_3 = os.path.join(dir_path, "pg_0003.json")
azure_page_test_4 = os.path.join(dir_path, "pg_0004.json")
azure_page_test_5 = os.path.join(dir_path, "pg_0005.json")



def test_page_test_1():
    test_1 = read_and_extract_page_two(azure_page_test_1)
    assert test_1 == {'Data': '29/04/2021', 'Q00': 'TWOR-BO1', 'Grup': 'BuxSon', 'Data Naix': '11/04/97', 'Q04': '74', 'Q02': 'MUJER', 'Q03': '165', 'Q05_full_text': 'NO', 'Q05': 1, 'Q06_full_text': 'SI, HEMITIROIDECTOMIA, MiOPIA', 'Q06': 1, 'Q07': 1, 'Q07_full_text': 'ESTACIONAL, POLVO', 'Q08': 1, 'Q08_full_text': 'ANTIHISTAMÍNICOS A DEMANDA', 'Q09': 0, 'Q09_full_text': 'NO _. Desde - hasta', 'Q10': 1, 'Q11': 0, 'Q12': 0, 'Q13': 0, 'Q14': 0, 'Q15': 0, 'Q17_Bdi': 0, 'Q16_Bso': 3, 'Q17': 0, 'Q20': 3, 'Q21': 0, 'Q22': 0, 'Q22_full_text': 'Desde hasta -'}

def test_page_test_2():
    test_2 = read_and_extract_page_two(azure_page_test_2)

    assert test_2 == {'Data': '30/4/21', 'Q00': 'BOZ', 'Grup': 'Bux', 'Data Naix': '2/2/97', 'Q04': '0.1)', 'Q02': None, 'Q03': '170', 'Q05_full_text': 'Malfornacio de chiari - ¿ Ha sido operado alguna', 'Q05': 1, 'Q06_full_text': 'Carrots (1998)', 'Q06': 1, 'Q07': 0, 'Q07_full_text': 'NO.', 'Q08': 0, 'Q08_full_text': 'NO', 'Q09': 0, 'Q09_full_text': 'No _. Desde hasta', 'Q10': 0, 'Q11': 0, 'Q13': 1, 'Q14': 0, 'Q15': 0, 'Q17_Bdi': 0, 'Q16_Bso': 2, 'Q17': 0, 'Q20': 2, 'Q21': 0, 'Q22': 0, 'Q22_full_text': 'Desde hasta'}

def test_page_test_3():
    test_3 = read_and_extract_page_two(azure_page_test_3)

    assert test_3 == {'Data': '13/9/21', 'Q00': '019', 'Grup': 'TLA', 'Data Naix': '18/9/2022', 'Q04': 'anos', 'Q02': None, 'Q03': '170', 'Q05_full_text': 'NO', 'Q05': 1, 'Q06_full_text': 'NO', 'Q06': 1, 'Q07': 0, 'Q07_full_text': 'NO', 'Q08': 0, 'Q08_full_text': 'NO', 'Q09': 0, 'Q09_full_text': 'NO. Desde hasta · ¿ Consume alcohol, tabaco u', 'Q10': 0, 'Q11': 0, 'Q12': 0, 'Q13': 0, 'Q14': None, 'Q15': None, 'Q17_Bdi': None, 'Q16_Bso': 0, 'Q17': None, 'Q20': 0, 'Q21': 0}

def test_page_test_4():
    test_4 = read_and_extract_page_two(azure_page_test_4)

    assert test_4 == {'Data': '8/11/21', 'Q00': '028', 'Grup': 'Ja', 'Data Naix': '6/5/76', 'Q04': '74', 'Q02': None, 'Q03': '1,66', 'Q05_full_text': 'estrasiso', 'Q05': 1, 'Q06_full_text': 'estrabismo', 'Q06': 1, 'Q07': 0, 'Q07_full_text': 'No', 'Q08': 0, 'Q08_full_text': 'No', 'Q09': 0, 'Q09_full_text': 'NO . Desde hasta 191.91', 'Q10': 0, 'Q11': 0, 'Q13': 2, 'Q14': 0, 'Q15': None, 'Q17_Bdi': None, 'Q16_Bso': 0, 'Q17': None, 'Q20': 0, 'Q21': 0}

def test_page_test_5():
    test_5 = read_and_extract_page_two(azure_page_test_5)

    assert test_5 == {'Data': '28/2/22', 'Q00': '042', 'Grup': 'TCA', 'Data Naix': '28/10/93', 'Q04': '2', 'Q02': None, 'Q03': '156', 'Q05_full_text': 'No', 'Q05': 1, 'Q06_full_text': 'Auguest de pit', 'Q06': 1, 'Q07': 0, 'Q07_full_text': 'NO .', 'Q08': 1, 'Q08_full_text': 'Fluoxetina, tranquirazón, escitalopram.', 'Q09': 0, 'Q09_full_text': 'No. Desde hasta .', 'Q10': 0, 'Q11': 0, 'Q12': 0, 'Q13': 0, 'Q14': None, 'Q15': None, 'Q17_Bdi': None, 'Q16_Bso': None, 'Q17': None, 'Q20': None, 'Q21': None}