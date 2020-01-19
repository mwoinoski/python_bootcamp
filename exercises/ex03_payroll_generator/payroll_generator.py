"""
Functions to run a batch payroll generation process.
"""

from random import random

ss_tax_rate = 0.062
mc_tax_rate = 0.0145

# TODO: define a class named CheckPrinter

# TODO: convert the print_check function to a method of CheckPrinter
# HINT: add a parameter named `self` at the beginning of the parameter list
def print_check(payroll_check_data):
    # print(f'printing check: {payroll_check_data}')
    return True


# TODO: define a class named PayrollRecordValidator

# TODO: convert the validate_payroll_record function to a method of PayrollRecordValidator
# HINT: add a parameter named `self` at the beginning of the parameter list
def validate_payroll_record(payroll_record):
    is_valid = False
    if payroll_record:
        emp_id = payroll_record.get('id')
        hours = payroll_record.get('hours_worked')
        status = payroll_record.get('tax_status')

        is_valid = emp_id and emp_id > 0 and \
            hours is not None and 0 <= hours <= 168 and \
            status and status in 'SsMm'

    if not is_valid:
        print(f'ERROR: Payroll record {payroll_record} is invalid')

    return is_valid


# TODO: note the RecordReader class
class RecordReader:
    # TODO: RecordReader will delegate validation tasks to its PayrollRecordValidator
    record_validator: PayrollRecordValidator

    # TODO: note the defintion of the __init__ method
    def __init__(self):
        # TODO: here we create the PayrollRecordValidator object
        self.record_validator = PayrollRecordValidator()

    # TODO: note the defintion of the read_payroll_records method
    def read_payroll_records(self, input_stream):
        records = []
        row_num = 0
        for line in input_stream:
            if row_num > 0:  # skip header line
                line = line.strip()  # remove newline
                row = line.split(',')  # row is a list of string: ['123','40','M']
                record = {
                    'id': int(row[0]),
                    'hours_worked': float(row[1]),
                    'tax_status': row[2]
                }
                if self.record_validator.validate_payroll_record(record):
                    records.append(record)
                else:
                    print(f'ERROR: skipping payroll record {line}')
            row_num += 1
        return records


# TODO: define a class named EmployeeDao

# TODO: convert the update_employee_record function to a method of EmployeeDao
def update_employee_record(emp_id, gross_pay, total_deductions):
    # should update employee record in the database
    return True


# TODO: define a class named PayCalculator

    # TODO: define a field named employee_dao, which is an EmployeeDao object


    # TODO: define an __init__ method

        # TODO: in the __init__ method, create an EmployeeDao object and
        #       assign it to self.employee_dao

# TODO: convert the 6 following calculate_* functions to methods of PayCalculator
# HINT: when one method calls another method, remember to use `self.` as a prefix:
#       gross_pay = self.calculate_gross_pay(...)
# HINT: when a method calls a method on another object, such as employee_dao,
#       use the object reference as a prefix:
#       this.employee_dao.update_employee_record(...)

def calculate_net_pay(pay_record):
    emp_id = pay_record['id']
    gross_pay = calculate_gross_pay(emp_id, pay_record['hours_worked'])
    total_deductions = calculate_deductions(
        emp_id, gross_pay, pay_record['tax_status'])
    update_employee_record(emp_id, gross_pay, total_deductions)
    net_pay = gross_pay - total_deductions

    return emp_id, round(gross_pay, 2), \
        round(total_deductions, 2), round(net_pay, 2)


def calculate_gross_pay(emp_id, hours_worked):
    # should lookup hourly rate from database
    return hours_worked * (15.0 + 75 * random())


def calculate_deductions(emp_id, gross_pay, tax_status):
    tax_withheld = calculate_tax_withheld(emp_id, gross_pay, tax_status)
    ss_withheld = calculate_ss_withheld(gross_pay)
    mc_withheld = calculate_mc_withheld(gross_pay)
    return tax_withheld + ss_withheld + mc_withheld


def calculate_tax_withheld(emp_id, gross_pay, tax_status):
    # should get tax rate based on tax status
    tax_withheld = gross_pay * (0.10 + 0.15 * random())
    return tax_withheld


def calculate_ss_withheld(gross_pay):
    ss_withheld = gross_pay * ss_tax_rate
    return ss_withheld


def calculate_mc_withheld(gross_pay):
    mc_withheld = gross_pay * mc_tax_rate
    return mc_withheld


# TODO: when you have completed the PayCalculator class, go to
#       test_payroll_generator.py and delete the @mark.skip decorator on the
#       four tests for PayCalculator. Run the unit tests with pytest and
#       verify that they all pass.

# TODO: note the definition of the PayrollProcess class

class PayrollProcessor:
    reader: RecordReader
    validator: PayrollRecordValidator
    calculator: PayCalculator
    check_printer: CheckPrinter

    def __init__(self):
        # TODO: create a RecordReader object and assign it to self.reader

        # TODO: create a PayCalculator object and assign it to self.calculator

        # TODO: create a CheckPrinter object and assign it to self.check_printer

    # TODO: this is the main processing method of the PayrollProcessor class
    def process_payroll_file(self, input_file_path):
        with open(input_file_path) as input_stream:
            # TODO: note how the current method calls another method
            return self.process_payroll_stream(input_stream)

    # TODO: this is the "easy to unit test" version of the main processing method
    def process_payroll_stream(self, input_stream):
        valid_records = []

        # TODO: note the call to self.read.read_payroll_records
        for record in self.reader.read_payroll_records(input_stream):
            valid_records.append(record)

            # TODO: note the call to self.calculator.calculate_net_pay
            payroll_check_data = self.calculator.calculate_net_pay(record)

            # TODO: note the call to self.check_printer.print_check
            check_printed = self.check_printer.print_check(payroll_check_data)

            print(f'check {"not" if not check_printed else payroll_check_data} '
                  f'printed for {record}')

        return valid_records

# TODO: when you have completed the PayrollProcessor class, go to
#       test_payroll_generator.py and delete the @mark.skip decorator on the
#       two tests for PayrollProcessor. Run the unit tests with pytest and
#       verify that they all pass.
