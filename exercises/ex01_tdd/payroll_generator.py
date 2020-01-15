"""
Functions to run a batch payroll generation process.
"""
import sys
from datetime import datetime


def main(input_file_path):
    for validated_record in get_payroll_records(input_file_path):
        payroll_check_data = calculate_net_pay(validated_record)
        check_printed = print_check(payroll_check_data)
        print(f'check {"not " if not check_printed else ""} printed '
              f'for ID {validated_record["id"]}')


def get_payroll_records(input_file_path):
    for payroll_record in read_payroll_records(input_file_path):
        record_valid = validate_payroll_record(payroll_record)
        if record_valid:
            yield payroll_record


def read_payroll_records(input_file_path):
    with open(input_file_path) as input_stream:
        records = []
        row_num = 0
        for line in input_stream:
            if row_num > 0:  # skip header line
                line = line.strip()  # remove newline
                row = line.split(',')  # row is a list of string: ['123','40','M']
                record = {'id': int(row[0]),
                          'hours_worked': float(row[1]),
                          'tax_status': row[2]}
                records.append(record)
            row_num += 1
    return records


# TODO: write unit tests for validate_payroll_record
def validate_payroll_record(payroll_record):
    emp_id = payroll_record.get('id')
    hours = payroll_record.get('hours_worked')
    status = payroll_record.get('tax_status')

    return emp_id and emp_id > 0 and \
        hours and 0 < hours <= 168 and \
        status and status in ('S', 'M')


def calculate_net_pay(validated_record):
    emp_id = validated_record['id']
    gross_pay = calculate_gross_pay(emp_id, validated_record['hours_worked'])
    total_deductions = calculate_deductions(emp_id, gross_pay,
                                            validated_record['tax_status'])
    update_employee_record(emp_id, gross_pay, total_deductions)
    net_pay = gross_pay - total_deductions
    return emp_id, gross_pay, total_deductions, net_pay


def calculate_gross_pay(emp_id, hours_worked):
    return hours_worked * 50.0  # should lookup hourly rate from database


def calculate_deductions(emp_id, gross_pay, tax_status):
    tax_withheld = calculate_tax_withheld(emp_id, gross_pay, tax_status)
    ss_withheld = calculate_ss_withheld(gross_pay)
    mc_withheld = calculate_mc_withheld(gross_pay)
    return tax_withheld + ss_withheld + mc_withheld


def calculate_tax_withheld(emp_id, gross_pay, tax_status):
    tax_withheld = gross_pay * 0.15  # should get tax rate based on tax status
    return tax_withheld


def calculate_ss_withheld(gross_pay):
    ss_withheld = gross_pay * 0.062
    return ss_withheld


def calculate_mc_withheld(gross_pay):
    mc_withheld = gross_pay * 0.0145
    return mc_withheld


def update_employee_record(emp_id, gross_pay, total_deductions):
    print(f'updating employee record: id={emp_id}, gross pay={gross_pay}, '
          f'deductions={total_deductions}')


def print_check(payroll_check_data):
    print(f'printing check: {payroll_check_data}')
    return True


if __name__ == '__main__':
    print('Payroll Generator batch process started at %s', datetime.now())

    main(sys.argv[1])
