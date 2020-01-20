from payroll_generator.employee_dao import DaoError


class PayrollGenerator:
    def __init__(self, employee_dao, pay_calculator, check_printer):
        self.employee_dao = employee_dao
        self.pay_calculator = pay_calculator
        self.check_printer = check_printer

    def generate_payroll(self):
        try:
            self.employee_dao.start_payroll_batch()

            valid_payroll_records = self.employee_dao.get_valid_payroll_records()

            valid_record_count, processed_rec_count, printed_check_count = \
                self.process_payroll_records(valid_payroll_records)

            self.employee_dao.end_payroll_batch()

            return self.employee_dao.get_payroll_batch_size(), \
                valid_record_count, processed_rec_count, printed_check_count

        except DaoError as de:
            raise PayrollGeneratorError from de

    def process_payroll_records(self, valid_payroll_records):
        valid_rec_count = 0
        processed_rec_count = 0
        printed_check_count = 0

        for payroll_record in valid_payroll_records:
            valid_rec_count += 1

            processed_ok, printed_ok = \
                self.process_payroll_record(payroll_record)

            processed_rec_count += 1 if processed_ok else 0
            printed_check_count += 1 if printed_ok else 0

        return valid_rec_count, processed_rec_count, printed_check_count

    def process_payroll_record(self, payroll_record):
        printed = False
        payroll_check_data = \
            self.pay_calculator.calculate_net_pay(payroll_record)
        if payroll_check_data:
            printed = self.check_printer.print_check(payroll_check_data)
        return payroll_check_data is not None, printed


class PayrollGeneratorError(Exception):
    pass
