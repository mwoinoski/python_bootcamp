"""
Unit tests for person_utils.py
"""
from person_utils import get_full_name

def test_get_full_name_success():
    full_name = get_full_name('Homer', 'John', 'Simpson')

    assert full_name == 'Homer John Simpson'

def test_get_full_name_success_2():
    full_name = get_full_name('Marge', 'Jane', 'Simpson')

    assert full_name == 'Marge Jane Simpson'

def test_get_full_name_success_family_is_a_num():
    full_name = get_full_name('Marge', 'Simpson', 3)
    assert full_name == 'Marge Simpson 3'

def test_get_full_name_success_quote():
    full_name = get_full_name('Marge', 'Jane', "O'Riley")
    assert full_name == "Marge Jane O'Riley"

def test_get_full_name_success_quote():
    full_name = get_full_name('Marge', None, "O'Riley")
    assert full_name == "Marge O'Riley"

def test_get_full_name_success_one_name():
    full_name = get_full_name('Madonna', None, None)
    assert full_name == "Madonna"



