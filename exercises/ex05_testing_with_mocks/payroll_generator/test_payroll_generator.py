from unittest.mock import Mock
from pytest import raises
from payroll_generator.employee_dao import DaoError
from payroll_generator.payroll_generator import PayrollGenerator, PayrollGeneratorError


class TestPayrollGenerator:

    # TODO: open payroll_generator.py and review the code of the PayrollGenerator
    #       class. Note that it calls methods of its dependencies, which are
    #       EmployeeDao, PayCalculator, and CheckPrinter objects. Our
    #       unit tests need to replace the "real" objects with mock objects.

    def test_payroll_generator_all_records_valid(self):
        # TODO: note how we create mock objects for all the PayrollGenerator's dependencies
        employee_dao = Mock()
        pay_calculator = Mock()
        check_printer = Mock()

        # TODO: note how we tell the mock employee_dao what its return value
        #       should be when its get_valid_payroll_records method is called
        employee_dao.get_valid_payroll_records.return_value = ['emp record'] * 1000
        # [value] * 1000 creates a list with 1000 copies of value

        # TODO: note how we tell the other mock objects what values to return
        #       when their methods are called
        employee_dao.get_payroll_batch_size.return_value = 1000
        pay_calculator.calculate_net_pay.return_value = 'payroll check'
        check_printer.print_check.return_value = 1

        # TODO: note how we pass the three mock objects to the PayrollGenerator constructor
        payroll_generator = PayrollGenerator(employee_dao, pay_calculator, check_printer)

        # TODO: note the call to the PayrollGenerator's generate_payroll method
        rec_count, valid_rec_count, check_data_count, printed_check_count = \
            payroll_generator.generate_payroll()

        # TODO: note how we verify that the PayrollGenerator code handled the
        #       return values from the mock objects correctly
        assert rec_count == 1000
        assert valid_rec_count == 1000
        assert check_data_count == 1000
        assert printed_check_count == 1000

    def test_payroll_generator_one_invalid_record(self):
        # TODO: in this test case, you will verify that the PayrollGenerator
        #       correctly handles the scenario where the input contains 1 invalid record
        # HINT: copy the first test case and change values where needed

        # TODO: create mock objects for all the PayrollGenerator's dependencies
        ....

        # TODO: tell the mock employee_dao to return 999 records
        #       when its get_valid_payroll_records method is called
        ....

        # TODO: tell the other mock objects to return the same values as the
        #       first test case. (In particular, employee_dao.get_payroll_batch_size
        #       should still return 1000).
        ....

        # TODO: call the PayrollGenerator constructor, passing the 3 mock objects
        #       as argments
        ....

        # TODO: call the PayrollGenerator's generate_payroll method
        ....

        # TODO: verify that the PayrollGenerator code handled the
        #       return values from the mock objects correctly.
        #       rec_count should be 1000
        #       The other values should be 999
        ....

    # TODO: after the previous test cases passes,
    #       uncomment the following test case, and then complete the code

    # def test_payroll_generator_employee_dao_raises_exception(self):
    #     # TODO: this test case will verify that when the EmployeeDao raises an
    #     #       exception, the PayrollGenerator correctly responds by raising
    #     #       a PayrollGeneratorError
    #
    #     employee_dao = Mock()
    #     pay_calculator = Mock()
    #     check_printer = Mock()
    #
    #     payroll_generator = PayrollGenerator(employee_dao, pay_calculator, check_printer)
    #
    #     # TODO: tell the employee_dao that a call to its get_valid_payroll_records
    #     #       should have the side effect of raising a DaoError
    #     employee_dao.get_valid_payroll_records.side_effect = DaoError()
    #
    #     # TODO: use the pytest `raises` function to detect a PayrollGeneratorError
    #     with raises(PayrollGeneratorError):
    #         # TODO: call the payroll_generator.generate_payroll method
    #         # HINT: you don't need to store the method's return value because
    #         #       it will never be used
    #         payroll_generator.generate_payroll()

    # --------------------------------------------------------------------------
    # TODO: Review the following completed test cases and be sure you
    #       understand how they work
    # --------------------------------------------------------------------------

    # TODO: We need to do the same setup for each unit test. To avoid duplicating
    #       code, you can a define a method named setup_method, which pytest
    #       will call before every test case.
    def setup_method(self, method):
        # Create the 3 mock objects and store them as attributes in the test class.
        self.employee_dao = Mock()
        self.pay_calculator = Mock()
        self.check_printer = Mock()

        # Create a PayrollGenerator with the mock objects as its dependencies
        self.payroll_generator = PayrollGenerator(
            self.employee_dao, self.pay_calculator, self.check_printer)

    def test_payroll_generator_net_pay_calc_fails_last_time(self):
        # TODO: note how the test case accesses the mock objects and PayrollGenerator
        #       that were initialized in the setup_method
        self.employee_dao.get_valid_payroll_records.return_value = ['emp record'] * 1000
        self.employee_dao.get_payroll_batch_size.return_value = 1000

        # For calculate_net_pay, set side_effect instead of return_value.
        # If side_effect is an iterable (for example, a list), each call to the
        # mock returns the next value.
        # So the calculate_net_pay method will return 'payroll check'
        # the first 999 times it is called, then it will return None the last time.
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
        # the print_check method will return 1 the first 999 times it is called,
        # then it will return 0 the last time
        self.check_printer.print_check.side_effect = [1] * 999 + [0]

        payroll_record_count, valid_payroll_record_count, \
            payroll_check_data_record_count, printed_check_count = \
            self.payroll_generator.generate_payroll()

        assert payroll_record_count == 1000
        assert valid_payroll_record_count == 1000
        assert payroll_check_data_record_count == 1000
        assert printed_check_count == 999
