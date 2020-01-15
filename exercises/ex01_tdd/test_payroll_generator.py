"""
Unit tests for payroll generator functions.
"""

from payroll_generator import generate_payroll

def test_payroll_generator_all_records_valid():

    payroll_record_count, valid_payroll_record_count, \
        payroll_check_data_record_count, printed_check_count = \
        generate_payroll()

    assert payroll_record_count == 1000
    assert valid_payroll_record_count == 1000
    assert payroll_check_data_record_count == 1000
    assert printed_check_count == 1000


def test_payroll_generator_one_invalid_record():

    payroll_record_count, valid_payroll_record_count, \
        payroll_check_data_record_count, printed_check_count = \
        generate_payroll()

    assert payroll_record_count == 1000
    assert valid_payroll_record_count == 999
    assert payroll_check_data_record_count == 999
    assert printed_check_count == 999


def test_payroll_generator_net_pay_calc_fails_last_time():

    payroll_record_count, valid_payroll_record_count, \
        payroll_check_data_record_count, printed_check_count = \
        generate_payroll()

    assert payroll_record_count == 1000
    assert valid_payroll_record_count == 1000
    assert payroll_check_data_record_count == 999
    assert printed_check_count == 999


def test_payroll_generator_print_check_fails_last_time():
    payroll_record_count, valid_payroll_record_count, \
        payroll_check_data_record_count, printed_check_count = \
        generate_payroll()

    assert payroll_record_count == 1000
    assert valid_payroll_record_count == 1000
    assert payroll_check_data_record_count == 1000
    assert printed_check_count == 999

# MW FIXME: copy contents of ex01_unit_testing/test_payroll.py here
