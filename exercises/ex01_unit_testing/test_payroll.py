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

