"""
Test error handling in the invoice handling code.
"""


from datetime import date, timedelta
from pytest import mark, raises

from invoice import Invoice


class TestInvoice:
    def test_constructor_id_one(self):
        invoice = Invoice(1, 'Awesome Medical Supply', date.today())
        assert invoice

    def test_constructor_id_zero(self):
        # TODO: put these statements inside a `try` statement
        try:
            invoice = Invoice(0, 'Awesome Medical Supply', date.today())
            assert invoice

        # TODO: add an `except` statement for ValueError, and
        #       print an appropriate error message
        except ValueError as ex:
            print(f'\ngot a ValueError: {ex}')

        # TODO: add a `finally` statement, and
        #       print an appropriate error message
        finally:
            print('Execution reached "finally" statement')

    # @mark.skip
    def test_constructor_payee_empty(self):
        # TODO: put these statements inside a `try` statement.
        #       Add a suitable `except` statement and a `finally` statement
        try:
            invoice = Invoice(123, '', date.today())
            assert invoice
        except ValueError as ex:
            print(f'\ngot a ValueError: {ex}')
        finally:
            print('Execution reached "finally" statement')

    def test_constructor_release_cutoff_none(self):
        with raises(ValueError):
            invoice = Invoice(123, 'Awesome Medical Supply', None)

    def test_constructor_release_cutoff_yesterday(self):
        with raises(ValueError):
            invoice = Invoice(123, 'Awesome Medical Supply',
                              date.today() - timedelta(days=1))

    def test_constructor_release_cutoff_today(self):
        invoice = Invoice(123, 'Awesome Medical Supply',
                          date.today())
        assert invoice

    def test_constructor_release_cutoff_tomorrow(self):
        invoice = Invoice(123, 'Awesome Medical Supply',
                          date.today() + timedelta(days=1))
        assert invoice
