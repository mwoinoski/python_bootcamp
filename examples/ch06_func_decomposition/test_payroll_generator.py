from unittest.mock import Mock
from pytest import raises
from employee_dao import DaoError
from payroll_generator import PayrollGenerator, PayrollGeneratorError


class TestPayrollGenerator:
    def setup_method(self, method):
        self.employee_dao = Mock(name='employee_dao')
        self.pay_calculator = Mock(name='pay_calculator')
        self.check_printer = Mock(name='check_printer')
        self.payroll_generator = PayrollGenerator(
            self.employee_dao, self.pay_calculator, self.check_printer)

    def test_payroll_generator_all_records_valid(self):
        # [value] * 1000 creates a list with 1000 copies of value
        self.employee_dao.get_valid_payroll_records.return_value = ['emp record'] * 1000
        self.employee_dao.get_payroll_batch_size.return_value = 1000
        self.pay_calculator.calculate_net_pay.return_value = 'payroll check'
        self.check_printer.print_check.return_value = 1

        payroll_record_count, valid_payroll_record_count, \
            payroll_check_data_record_count, printed_check_count = \
            self.payroll_generator.generate_payroll()

        assert payroll_record_count == 1000
        assert valid_payroll_record_count == 1000
        assert payroll_check_data_record_count == 1000
        assert printed_check_count == 1000

    def test_payroll_generator_one_invalid_record(self):
        self.employee_dao.get_valid_payroll_records.return_value = ['emp record'] * 999
        self.employee_dao.get_payroll_batch_size.return_value = 1000
        self.pay_calculator.calculate_net_pay.return_value = 'payroll check'
        self.check_printer.print_check.return_value = 1

        payroll_record_count, valid_payroll_record_count, \
            payroll_check_data_record_count, printed_check_count = \
            self.payroll_generator.generate_payroll()

        assert payroll_record_count == 1000
        assert valid_payroll_record_count == 999
        assert payroll_check_data_record_count == 999
        assert printed_check_count == 999

    def test_payroll_generator_net_pay_calc_fails_last_time(self):
        self.employee_dao.get_valid_payroll_records.return_value = ['emp record'] * 1000
        self.employee_dao.get_payroll_batch_size.return_value = 1000
        # for calculate_net_pay, set side_effect instead of return value.
        # if side_effect is an iterable, each call to the mock returns the next value.
        self.pay_calculator.calculate_net_pay.side_effect = ['payroll check'] * 999 + [None]
        self.check_printer.print_check.return_value = 1

        payroll_record_count, valid_payroll_record_count, \
            payroll_check_data_record_count, printed_check_count = \
            self.payroll_generator.generate_payroll()

        assert payroll_record_count == 1000
        assert valid_payroll_record_count == 1000
        assert payroll_check_data_record_count == 999
        assert printed_check_count == 999

    def test_payroll_generator_print_check_fails_last_time(self):
        self.employee_dao.get_valid_payroll_records.return_value = ['emp record'] * 1000
        self.employee_dao.get_payroll_batch_size.return_value = 1000
        self.pay_calculator.calculate_net_pay.return_value = ['payroll check']
        self.check_printer.print_check.side_effect = [1] * 999 + [0]

        payroll_record_count, valid_payroll_record_count, \
            payroll_check_data_record_count, printed_check_count = \
            self.payroll_generator.generate_payroll()

        assert payroll_record_count == 1000
        assert valid_payroll_record_count == 1000
        assert payroll_check_data_record_count == 1000
        assert printed_check_count == 999

    def test_payroll_generator_print_check_fails_last_time(self):
        self.employee_dao.get_valid_payroll_records.side_effect = DaoError()

        with raises(PayrollGeneratorError):
            self.payroll_generator.generate_payroll()
