"""
Unit tests for payroll generator functions
"""

from payroll import validate_payroll_record


def test_validate_payroll_record_all_fields_valid_true():
    pay_rec = {'id': 123, 'hours_worked': 40, 'tax_status': 'S'}
    assert validate_payroll_record(pay_rec)


# TODO: add test cases to this file to thoroughly test the
# validate_payroll_record function in payroll.py.
# Use the test case above as a template for your tests.

def test_validate_payroll_record_min_id_true():
    pay_rec = {'id': 1, 'hours_worked': 40, 'tax_status': 'S'}
    assert validate_payroll_record(pay_rec)


def test_validate_payroll_record_min_hours_true():
    pay_rec = {'id': 123, 'hours_worked': 0, 'tax_status': 'S'}
    assert validate_payroll_record(pay_rec)


def test_validate_payroll_record_max_hours_true():
    pay_rec = {'id': 123, 'hours_worked': 168, 'tax_status': 'S'}
    assert validate_payroll_record(pay_rec)


def test_validate_payroll_record_status_married_true():
    pay_rec = {'id': 123, 'hours_worked': 168, 'tax_status': 'M'}
    assert validate_payroll_record(pay_rec)


def test_validate_payroll_record_id_missing_false():
    pay_rec = {'hours_worked': 40, 'tax_status': 'S'}
    assert not validate_payroll_record(pay_rec)


def test_validate_payroll_record_bad_id_false():
    pay_rec = {'id': 0, 'hours_worked': 40, 'tax_status': 'S'}
    assert not validate_payroll_record(pay_rec)


def test_validate_payroll_record_hours_missing_false():
    pay_rec = {'id': 0, 'tax_status': 'S'}
    assert not validate_payroll_record(pay_rec)


def test_validate_payroll_record_hours_below_min_false():
    pay_rec = {'id': 0, 'hours_worked': -1, 'tax_status': 'S'}
    assert not validate_payroll_record(pay_rec)


def test_validate_payroll_record_hours_above_max_false():
    pay_rec = {'id': 0, 'hours_worked': 168.1, 'tax_status': 'S'}
    assert not validate_payroll_record(pay_rec)


def test_validate_payroll_record_status_missing_false():
    pay_rec = {'id': 0, 'hours_worked': 40}
    assert not validate_payroll_record(pay_rec)


def test_validate_payroll_record_bad_status_false():
    pay_rec = {'id': 0, 'hours_worked': 40, 'tax_status': 'X'}
    assert not validate_payroll_record(pay_rec)


def test_validate_payroll_record_empty_record_false():
    pay_rec = {}
    assert not validate_payroll_record(pay_rec)


def test_validate_payroll_record_arg_none_false():
    pay_rec = None
    assert not validate_payroll_record(pay_rec)
