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
        invoice = Invoice(0, 'Awesome Medical Supply', date.today())
        assert invoice

        # TODO: add an `except` statement for ValueError, and
        #       print an appropriate error message


        # TODO: add a `finally` statement, and
        #       print an appropriate error message


    # @mark.skip
    def test_constructor_payee_empty(self):
        # TODO: put these statements inside a `try` statement.
        #       Add a suitable `except` statement and a `finally` statement

        invoice = Invoice(123, '', date.today())
        assert invoice
