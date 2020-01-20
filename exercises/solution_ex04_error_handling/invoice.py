"""
Invoice class example from chapter 4.
Demonstrates raising exceptions and the `try` statement.
"""

from datetime import date
from typing import Any

from invoice_data_access_object import InvoiceDataAccessObject


class InvoiceProcessingError(Exception):
    """ User-defined exception class """
    pass


class Invoice:
    invoice_id: int
    payee: str
    release_cutoff_date: date
    dao: Any

    def __init__(self, invoice_id: int, payee: str, release_cutoff_date: date):

        if not invoice_id or invoice_id <= 0:
            raise ValueError(f'invalid invoice ID {invoice_id}')

        # TODO: if payee is None or an empty string, raise a ValueError
        if not payee:
            raise ValueError(f"payee can't be empty")

        # TODO: if release_cutoff is not set or if it is earlier than today,
        #       raise a ValueError
        # HINT: you can compare two dates with the '<' operator, like this:
        #       release_cutoff < date.today()
        if not release_cutoff_date or release_cutoff_date < date.today():
            raise ValueError(f'invalid release cutoff date {release_cutoff_date}')

        self.invoice_id = invoice_id
        self.release_cutoff_date = release_cutoff_date
        self.dao = InvoiceDataAccessObject()

    def release(self):
        if not self.is_ok_to_release():
            msg = f"invoice {self.invoice_id} can't be released"
            raise InvoiceProcessingError(msg)

        return self.dao.set_released_status(self)

    def is_ok_to_release(self) -> bool:
        try:
            status = self.dao.lookup_status(self.invoice_id)
            return status == 1 and self.release_cutoff >= date.today()
        except ValueError as ve:
            print(f'ValueError: {ve}')
            return False
        except Exception as ex:
            print(f'Exception: {ex}')
            return False
        finally:
            print('Execution reached "finally" statement')


if __name__ == '__main__':
    release_cutoff_date = date(2021, 12, 31)
    dao = InvoiceDataAccessObject()

    invoice = Invoice(1123, release_cutoff_date, dao)

    un = '' if invoice.is_ok_to_release() else 'un'
    print(f'invoice is {un}released')
    print('Done processing invoice')
