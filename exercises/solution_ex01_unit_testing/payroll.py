"""
Functions for generating payroll process.
"""


def validate_payroll_record(payroll_record):
    if not payroll_record:
        return False

    emp_id = payroll_record.get('id')
    hours = payroll_record.get('hours_worked')
    status = payroll_record.get('tax_status')

    return emp_id and emp_id > 0 and \
        hours is not None and 0 <= hours <= 168 and \
        status and status in ('S', 'M')
