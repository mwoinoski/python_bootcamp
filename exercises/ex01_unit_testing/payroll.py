"""
Functions for generating payroll process.
"""


# TODO: write unit tests for validate_payroll_record
def validate_payroll_record(payroll_record):
    emp_id = payroll_record.get('id')
    hours = payroll_record.get('hours_worked')
    status = payroll_record.get('tax_status')

    return emp_id and emp_id > 0 and \
        hours and 0 <= hours <= 168 and \
        status and status in ('S', 'M')


def get_payroll_records():
    recs = []
    for payroll_record in read_payroll_records():
        record_valid = validate_payroll_record(payroll_record)
        if record_valid:
            recs.append(payroll_record)
    return recs


def read_payroll_records():  # dummy function to query database
    return [
        {'id': 1, 'hours_worked': 40, 'tax_status': 'S'},
        {'id': 2, 'hours_worked': 35, 'tax_status': 'M'},
        {'id': 3, 'hours_worked': 45, 'tax_status': 'M'},
    ]



