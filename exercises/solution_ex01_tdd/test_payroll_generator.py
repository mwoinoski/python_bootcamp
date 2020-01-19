"""
Unit tests for payroll generator functions.
"""

from pytest import approx
import payroll_generator
from payroll_generator import (
    validate_payroll_record, calculate_net_pay, ss_tax_rate, mc_tax_rate
)


# TODO: this test case reproduces the bug
def test_validate_payroll_record_status_lower_case_true():
    pay_rec = {'id': 123, 'hours_worked': 40, 'tax_status': 'm'}
    assert validate_payroll_record(pay_rec)


def test_validate_payroll_record_all_fields_valid_true():
    pay_rec = {'id': 123, 'hours_worked': 40, 'tax_status': 'S'}
    assert validate_payroll_record(pay_rec)


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


mock_hourly_rate = 50.0
mock_tax_rate = 0.15


def test_calculate_net_pay_40_hours_single(monkeypatch):
    setup_monkeypatch(monkeypatch)

    pay_rec = {'id': 123, 'hours_worked': 40, 'tax_status': 'S'}

    results = calculate_net_pay(pay_rec)

    gross = 40 * mock_hourly_rate
    deductions = gross * mock_tax_rate + gross * ss_tax_rate + gross * mc_tax_rate
    expected = (123, approx(gross, abs=0.005), approx(deductions, abs=0.005),
                approx(gross - deductions, abs=0.005))
    assert results == expected


def test_calculate_net_pay_40_hours_married(monkeypatch):
    setup_monkeypatch(monkeypatch)

    pay_rec = {'id': 123, 'hours_worked': 40, 'tax_status': 'M'}

    results = calculate_net_pay(pay_rec)

    gross = 40 * mock_hourly_rate
    deductions = gross * mock_tax_rate + gross * ss_tax_rate + gross * mc_tax_rate
    expected = (123, approx(gross, abs=0.005), approx(deductions, abs=0.005),
                approx(gross - deductions, abs=0.005))
    assert results == expected


def test_calculate_net_pay_1_hour_single(monkeypatch):
    setup_monkeypatch(monkeypatch)

    pay_rec = {'id': 123, 'hours_worked': 1, 'tax_status': 'S'}

    results = calculate_net_pay(pay_rec)

    gross = 1 * mock_hourly_rate
    deductions = gross * mock_tax_rate + gross * ss_tax_rate + gross * mc_tax_rate
    expected = (123, approx(gross, abs=0.005), approx(deductions, abs=0.005),
                approx(gross - deductions, abs=0.005))
    assert results == expected


def test_calculate_net_pay_0_hour_single(monkeypatch):
    setup_monkeypatch(monkeypatch)

    pay_rec = {'id': 123, 'hours_worked': 0, 'tax_status': 'S'}

    results = calculate_net_pay(pay_rec)

    assert results == (123, 0, 0, 0)


def setup_monkeypatch(monkeypatch):

    def mock_calculate_gross_pay(emp_id, hours_worked):
        return hours_worked * mock_hourly_rate

    def mock_calculate_tax_withheld(emp_id, gross_pay, tax_status):
        return gross_pay * mock_tax_rate

    monkeypatch.setattr(payroll_generator, "calculate_gross_pay",
                        mock_calculate_gross_pay)

    monkeypatch.setattr(payroll_generator, "calculate_tax_withheld",
                        mock_calculate_tax_withheld)


