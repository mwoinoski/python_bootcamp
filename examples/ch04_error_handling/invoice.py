"""
Invoice class example from chapter 4.
Demonstrates try statement.
"""

from datetime import date


class InvoiceDataAccessObject:
    def __init__(self) -> None:  # set up connection to DB
        self.usage_count = 0

    def lookup_status(self, invoice_id: int) -> int:
        if invoice_id < 1:
            raise ValueError(f'invalid invoice_id {invoice_id}')

        self.usage_count += 1
        return self.usage_count


class Invoice:
    invoice_id: int
    release_cutoff: date
    dao: InvoiceDataAccessObject

    def __init__(self, invoice_id: int, cutoff: date, dao) -> None:
        self.invoice_id = invoice_id
        self.release_cutoff = cutoff
        self.dao = dao

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
