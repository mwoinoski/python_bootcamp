"""
Demo of user-defined exceptions in chapter 4.
Here, the exception handler raises a new exception.
"""

import sys
from dataclasses import dataclass
from datetime import date


class DaoError(Exception):
    pass


@dataclass
class InvoiceDao:
    db_name: str

    def lookup_status(self, inv_id: int):
        if inv_id < 1:
            raise DaoError(f'invalid invoice ID {inv_id}')
        return 1

    def close(self):
        print(f'InvoiceDao {self.db_name} is closing')


@dataclass
class Invoice:
    invoice_id: int
    dao: InvoiceDao

    def is_invoice_released(self) -> bool:
        try:
            status = self.dao.lookup_status(self.invoice_id)
            return status == 1 and self.release_cutoff >= date.today()
        except DaoError as de:
            self.handle_bad_invoice_id()
            raise ValueError(str(de))

    def handle_bad_invoice_id(self):
        print(f'handling bad invoice ID {self.invoice_id}')


if __name__ == '__main__':
    try:
        invoice = Invoice(-1, InvoiceDao('InvoicesDB'))
        print(f'invoice is {"" if invoice.is_invoice_released() else "un"}'
              f'released')
    except ValueError as ve:
        print(f'ValueError: {ve}')
    except Exception:
        type, ex, traceback = sys.exc_info()
        ex_class_name = type.__name__
        print(f'{ex_class_name}: {ex}')

    print('Done with main')
