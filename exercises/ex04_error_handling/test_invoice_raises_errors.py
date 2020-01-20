"""
Test error handling in the invoice handling code.
"""


from datetime import date, timedelta
from pytest import raises

from invoice import Invoice


class TestInvoiceRaisesErrors:
    # TODO Step 1: add a new test method

        # TODO: in the new test method, call the `raises` function to check for a ValueError

            # TODO: call the Invoice constructor with a release_cutoff_date value of None


    # --------------------------------------------------------------------------
    # skip Step 2 until the first test case passes
    # --------------------------------------------------------------------------

    # TODO Step 2: add a new test method to verify if you pass a release cutoff value
    #       of yesterday's date to the Invoice constructor, it raises a ValueError
    # HINT: calculate yesterday's date like this:
    #       date.today() - timedelta(days=1)



    # TODO Step 2: add a new test method to verify if you pass a release cutoff date
    #       of today's date to the Invoice constructor, it succeeds




    # TODO Step 2: add a new test method to verify if you pass a release cutoff date
    #       of tomorrow's date to the Invoice constructor, it succeeds


