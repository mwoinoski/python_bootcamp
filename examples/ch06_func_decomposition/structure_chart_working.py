from datetime import datetime
import logging.config
from logging_decorator import log_call

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('payroll_generator')


@log_call()
def main():
    for validated_record in get_payroll_records():
        payroll_check_data = calculate_net_pay(validated_record)
        check_printed = print_check(payroll_check_data)
        logger.debug('check%s printed for ID %d',
                     '' if check_printed else ' not', validated_record['id'])


@log_call()
def get_payroll_records():
    for payroll_record in read_payroll_records():
        record_valid = validate_payroll_record(payroll_record)
        if record_valid:
            yield payroll_record


@log_call()
def read_payroll_records():
    return [
        {'id': 1, 'hours_worked': 40, 'tax_status': 'S'},
        {'id': 2, 'hours_worked': 35, 'tax_status': 'M'},
        {'id': 3, 'hours_worked': 45, 'tax_status': 'M'},
    ]  # FIXME


@log_call()
def validate_payroll_record(payroll_record):
    if payroll_record:  # FIXME
        return True
    else:
        return False


@log_call()
def calculate_net_pay(validated_record):
    emp_id = validated_record['id']
    gross_pay = calculate_gross_pay(emp_id, validated_record['hours_worked'])
    total_deductions = calculate_deductions(emp_id, gross_pay,
                                            validated_record['tax_status'])
    update_employee_record(emp_id, gross_pay, total_deductions)
    net_pay = gross_pay - total_deductions  # FIXME
    return emp_id, gross_pay, total_deductions, net_pay


@log_call()
def calculate_gross_pay(emp_id, hours_worked):
    return 1500.0  # FIXME


@log_call()
def calculate_deductions(emp_id, gross_pay, tax_status):
    tax_withheld = calculate_tax_withheld(emp_id, gross_pay, tax_status)
    ss_withheld = calculate_ss_withheld(gross_pay)
    mc_withheld = calculate_mc_withheld(gross_pay)
    return tax_withheld + ss_withheld + mc_withheld


@log_call()
def calculate_tax_withheld(emp_id, gross_pay, tax_status):
    tax_withheld = gross_pay * 0.15  # FIXME
    return tax_withheld


@log_call()
def calculate_ss_withheld(gross_pay):
    ss_withheld = gross_pay * 0.062  # FIXME
    return ss_withheld


@log_call()
def calculate_mc_withheld(gross_pay):
    mc_withheld = gross_pay * 0.0145  # FIXME
    return mc_withheld


@log_call()
def update_employee_record(emp_id, gross_pay, total_deductions):
    pass  # FIXME


@log_call()
def print_check(payroll_check_data):
    return True  # FIXME


if __name__ == '__main__':
    logger.info('Payroll Generator batch process started at %s', datetime.now())

    main()
