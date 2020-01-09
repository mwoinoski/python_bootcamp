class PayrollGenerator:
    def __init__(self, employee_dao, pay_calculator, check_printer):
        self.employee_dao = employee_dao
        self.pay_calculator = pay_calculator
        self.check_printer = check_printer

    def generate_payroll(self):
        payroll_check_data_record_count = 0
        printed_check_count = 0
        valid_payroll_record_count = 0

        self.employee_dao.start_payroll_batch()
        valid_payroll_records = self.employee_dao.get_valid_payroll_records()
        for payroll_record in valid_payroll_records:
            valid_payroll_record_count += 1
            payroll_check_data = self.pay_calculator.calculate_net_pay(payroll_record)
            if payroll_check_data:
                payroll_check_data_record_count += 1
                if self.check_printer.print_check(payroll_check_data):
                    printed_check_count += 1
        self.employee_dao.end_payroll_batch()

        return self.employee_dao.get_payroll_batch_size(), \
            valid_payroll_record_count, \
            payroll_check_data_record_count, \
            printed_check_count
