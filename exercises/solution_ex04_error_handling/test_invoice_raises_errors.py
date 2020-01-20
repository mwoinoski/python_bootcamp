"""
Test error handling in the invoice handling code.
"""


from datetime import date, timedelta
from pytest import raises

from invoice import Invoice


class TestInvoiceRaisesErrors:
    # TODO Step 1: add a new test method
    def test_constructor_release_cutoff_none(self):
        # TODO: in the new test method, call the `raises` function to check for a ValueError
        with raises(ValueError):
            # TODO: call the Invoice constructor with a release_cutoff_date value of None
            invoice = Invoice(123, 'Awesome Medical Supply', None)

    # --------------------------------------------------------------------------
    # skip TODO Step 2 until the first test case passes
    # --------------------------------------------------------------------------

    # TODO Step 2: add a new test method to verify if you pass a release cutoff value
    #       of yesterday's date to the Invoice constructor, it raises a ValueError
    # HINT: calculate yesterday's date like this:
    #       date.today() - timedelta(days=1)
    def test_constructor_release_cutoff_yesterday(self):
        with raises(ValueError):
            yesterday = date.today() - timedelta(days=1)
            invoice = Invoice(123, 'Awesome Medical Supply', yesterday)

    # TODO Step 2: add a new test method to verify if you pass a release cutoff date
    #       of today's date to the Invoice constructor, it succeeds
    def test_constructor_release_cutoff_today(self):
        invoice = Invoice(123, 'Awesome Medical Supply', date.today())
        assert invoice

    # TODO Step 2: add a new test method to verify if you pass a release cutoff date
    #       of tomorrow's date to the Invoice constructor, it succeeds
    def test_constructor_release_cutoff_tomorrow(self):
        tomorrow = date.today() + timedelta(days=1)
        invoice = Invoice(123, 'Awesome Medical Supply', tomorrow)
        assert invoice
