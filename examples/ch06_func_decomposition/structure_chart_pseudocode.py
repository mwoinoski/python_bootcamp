def main():
    for validated_record in get_payroll_records():
        payroll_check_data = calculate_net_pay(validated_record)
        check_printed = print_check(payroll_check_data)

def get_payroll_records():
    for payroll_record in read_payroll_records():
        record_valid = validate_payroll_record(payroll_record)
        if record_valid:
            yield payroll_record

def calculate_net_pay(validated_record):
    emp_id = validated_record['id']
    gross_pay = calculate_gross_pay(emp_id, validated_record['hours_worked'])
    total_deductions = calculate_deductions(emp_id, gross_pay,
                                            validated_record['tax_status'])
    update_employee_record(emp_id, gross_pay, total_deductions)
    net_pay = gross_pay - total_deductions  # FIXME
    return emp_id, gross_pay, total_deductions, net_pay

def print_check(payroll_check_data):
    return True  # FIXME

def read_payroll_records():
    return []  # FIXME

def validate_payroll_record(payroll_record):
    if payroll_record:  # FIXME
        return True
    else:
        return False

def calculate_gross_pay(emp_id, hours_worked):
    return 1500.0  # FIXME

def calculate_deductions(emp_id, gross_pay, tax_status):
    tax_withheld = calculate_tax_withheld(emp_id, gross_pay, tax_status)
    ss_withheld = calculate_ss_withheld(gross_pay)
    mc_withheld = calculate_mc_withheld(gross_pay)
    return tax_withheld + ss_withheld + mc_withheld

def calculate_tax_withheld(emp_id, gross_pay, tax_status):
    tax_withheld = gross_pay * 0.15  # FIXME
    return tax_withheld

def calculate_ss_withheld(gross_pay):
    ss_withheld = gross_pay * 0.062  # FIXME
    return ss_withheld

def calculate_mc_withheld(gross_pay):
    mc_withheld = gross_pay * 0.0145  # FIXME
    return mc_withheld

def update_employee_record(emp_id, gross_pay, total_deductions):
    pass  # FIXME
