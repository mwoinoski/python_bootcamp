"""
Driver for CSV Processor
"""

import sys
from datetime import datetime

# TODO: import PayrollProcessor from payroll_generator
from payroll_generator import PayrollProcessor

# TODO: delete the following import
from payroll_generator import process_payroll_file

if __name__ == '__main__':
    print(f'Payroll Generator batch process started at {datetime.now()}')

    # TODO: create an instance of PayrollProcessor and assign to a variable


    # TODO: use the variable you created above to call the PayrollProcessor's
    #       process_payroll_file method, passing sys.argv[1] as the argument


    # TODO: delete the following line of code
    process_payroll_file(sys.argv[1])
