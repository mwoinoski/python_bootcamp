"""
Unit tests for payroll generator functions.
"""

import io
import textwrap
from pytest import approx, mark
from payroll_generator import (
    PayrollProcessor, PayrollRecordValidator, PayCalculator,
    RecordReader, ss_tax_rate, mc_tax_rate
)


class TestPayrollProcessor:
    mock_hourly_rate: float = 50.0
    mock_tax_rate: float = 0.15

    # --------------------------------------------------------------------------
    # ----------------- tests for PayrollRecordValidator class -----------------
    # --------------------------------------------------------------------------

    def test_validate_payroll_record_all_fields_valid_true(self) -> None:
        pay_rec = {'id': 123, 'hours_worked': 40, 'tax_status': 'S'}

        validator = PayrollRecordValidator()

        assert validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_min_id_true(self) -> None:
        pay_rec = {'id': 1, 'hours_worked': 40, 'tax_status': 'S'}
        validator = PayrollRecordValidator()
        assert validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_min_hours_true(self) -> None:
        pay_rec = {'id': 123, 'hours_worked': 0, 'tax_status': 'S'}
        validator = PayrollRecordValidator()
        assert validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_max_hours_true(self) -> None:
        pay_rec = {'id': 123, 'hours_worked': 168, 'tax_status': 'S'}
        validator = PayrollRecordValidator()
        assert validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_status_married_true(self) -> None:
        pay_rec = {'id': 123, 'hours_worked': 168, 'tax_status': 'M'}
        validator = PayrollRecordValidator()
        assert validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_id_missing_false(self) -> None:
        pay_rec = {'hours_worked': 40, 'tax_status': 'S'}
        validator = PayrollRecordValidator()
        assert not validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_bad_id_false(self) -> None:
        pay_rec = {'id': 0, 'hours_worked': 40, 'tax_status': 'S'}
        validator = PayrollRecordValidator()
        assert not validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_hours_missing_false(self) -> None:
        pay_rec = {'id': 0, 'tax_status': 'S'}
        validator = PayrollRecordValidator()
        assert not validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_hours_below_min_false(self) -> None:
        pay_rec = {'id': 0, 'hours_worked': -1, 'tax_status': 'S'}
        validator = PayrollRecordValidator()
        assert not validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_hours_above_max_false(self) -> None:
        pay_rec = {'id': 0, 'hours_worked': 168.1, 'tax_status': 'S'}
        validator = PayrollRecordValidator()
        assert not validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_status_missing_false(self) -> None:
        pay_rec = {'id': 0, 'hours_worked': 40}
        validator = PayrollRecordValidator()
        assert not validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_bad_status_false(self) -> None:
        pay_rec = {'id': 0, 'hours_worked': 40, 'tax_status': 'X'}
        validator = PayrollRecordValidator()
        assert not validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_empty_record_false(self) -> None:
        pay_rec = {}
        validator = PayrollRecordValidator()
        assert not validator.validate_payroll_record(pay_rec)

    def test_validate_payroll_record_arg_none_false(self) -> None:
        pay_rec = None
        validator = PayrollRecordValidator()
        assert not validator.validate_payroll_record(pay_rec)

    # --------------------------------------------------------------------------
    # ----------------------- tests for PayCalculator class --------------------
    # --------------------------------------------------------------------------

    # @mark.skip()
    def test_calculate_net_pay_40_hours_single(self, monkeypatch):
        self.setup_monkeypatch(monkeypatch)

        pay_rec = {'id': 123, 'hours_worked': 40, 'tax_status': 'S'}

        pay_calculator = PayCalculator()
        results = pay_calculator.calculate_net_pay(pay_rec)

        gross = 40 * self.mock_hourly_rate
        deductions = gross * self.mock_tax_rate + gross * \
            ss_tax_rate + gross * mc_tax_rate
        expected = (123, approx(gross, abs=0.005), approx(deductions, abs=0.005),
                    approx(gross - deductions, abs=0.005))
        assert results == expected

    # @mark.skip()
    def test_calculate_net_pay_40_hours_married(self, monkeypatch):
        self.setup_monkeypatch(monkeypatch)

        pay_rec = {'id': 123, 'hours_worked': 40, 'tax_status': 'M'}

        pay_calculator = PayCalculator()
        results = pay_calculator.calculate_net_pay(pay_rec)

        gross = 40 * self.mock_hourly_rate
        deductions = gross * self.mock_tax_rate + gross * \
            ss_tax_rate + gross * mc_tax_rate
        expected = (123, approx(gross, abs=0.005), approx(deductions, abs=0.005),
                    approx(gross - deductions, abs=0.005))
        assert results == expected

    # @mark.skip()
    def test_calculate_net_pay_1_hour_single(self, monkeypatch):
        self.setup_monkeypatch(monkeypatch)

        pay_rec = {'id': 123, 'hours_worked': 1, 'tax_status': 'S'}

        pay_calculator = PayCalculator()
        results = pay_calculator.calculate_net_pay(pay_rec)

        gross = 1 * self.mock_hourly_rate
        deductions = gross * self.mock_tax_rate + gross * \
            ss_tax_rate + gross * mc_tax_rate
        expected = (123, approx(gross, abs=0.005), approx(deductions, abs=0.005),
                    approx(gross - deductions, abs=0.005))
        assert results == expected

    # @mark.skip()
    def test_calculate_net_pay_0_hour_single(self, monkeypatch):
        self.setup_monkeypatch(monkeypatch)

        pay_rec = {'id': 123, 'hours_worked': 0, 'tax_status': 'S'}

        pay_calculator = PayCalculator()
        results = pay_calculator.calculate_net_pay(pay_rec)

        assert results == (123, 0, 0, 0)

    def setup_monkeypatch(self, monkeypatch):

        def mock_calculate_gross_pay(obj, emp_id, hours_worked):
            return hours_worked * self.mock_hourly_rate

        def mock_calculate_tax_withheld(obj, emp_id, gross_pay, tax_status):
            return gross_pay * self.mock_tax_rate

        monkeypatch.setattr(PayCalculator, "calculate_gross_pay",
                            mock_calculate_gross_pay)

        monkeypatch.setattr(PayCalculator, "calculate_tax_withheld",
                            mock_calculate_tax_withheld)

    # --------------------------------------------------------------------------
    # --------------------- tests for PayrollProcessor class -------------------
    # --------------------------------------------------------------------------

    # @mark.skip()
    def test_read_csv_file_file_success(self) -> None:
        csv_file_path = 'payroll_recs_week_4.csv'

        payroll_processor = PayrollProcessor()

        valid_recs = payroll_processor.process_payroll_file(csv_file_path)

        assert len(valid_recs) == 7
        assert valid_recs[0] == {'id': 123, 'hours_worked': 40.0, 'tax_status': 'M'}
        assert valid_recs[6] == {'id': 891, 'hours_worked': 49.7, 'tax_status': 'S'}

    # @mark.skip()
    def test_process_csv_stream_success(self) -> None:
        csv_text = textwrap.dedent("""\
            ID,Hours Worked,Tax Status
            123,40.0,S
            234,39.1,M
            4321,44.5,S
            1013,0,M
        """)
        csv_input_stream = io.StringIO(csv_text)

        payroll_processor = PayrollProcessor()

        valid_recs = payroll_processor.process_payroll_stream(csv_input_stream)

        assert len(valid_recs) == 4
        assert valid_recs == [
            {'id': 123, 'hours_worked': 40.0, 'tax_status': 'S'},
            {'id': 234, 'hours_worked': 39.1, 'tax_status': 'M'},
            {'id': 4321, 'hours_worked': 44.5, 'tax_status': 'S'},
            {'id': 1013, 'hours_worked': 0, 'tax_status': 'M'},
        ]
