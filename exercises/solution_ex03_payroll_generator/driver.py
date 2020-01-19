"""
Driver for CSV Processor
"""

import sys
from datetime import datetime

# TODO: import PayrollProcessor from payroll_generator
from payroll_generator import PayrollProcessor

# TODO: delete the following import
# from payroll_generator import process_payroll_file

if __name__ == '__main__':
    print(f'Payroll Generator batch process started at {datetime.now()}')

    # TODO: create an instance of PayrollProcessor
    payroll_processor = PayrollProcessor()

    # TODO: call the PayrollProcessor's process_payroll_file method, passing
    #       sys.argv[1] as the argument
    payroll_processor.process_payroll_file(sys.argv[1])

    # TODO: delete the following line of code
    # process_payroll_file(sys.argv[1])
