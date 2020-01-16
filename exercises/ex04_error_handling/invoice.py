"""
Invoice class example from chapter 4.
Demonstrates try statement.
"""
from dataclasses import dataclass
from datetime import date

from invoice_data_access_object import InvoiceDataAccessObject


@dataclass
class Invoice:
    invoice_id: int
    release_cutoff: date
    dao: InvoiceDataAccessObject

    def is_invoice_released(self) -> bool:
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
    invoice = Invoice(0, date(2021, 12, 31), InvoiceDataAccessObject())
    un = '' if invoice.is_invoice_released() else 'un'
    print(f'invoice is {un}released')
    print('Done processing invoice')
