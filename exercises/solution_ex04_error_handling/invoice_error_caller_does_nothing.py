"""
Invoice class example from chapter 4.
Demonstrates unhandled exceptions.
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

    def __init__(self, inv_id: int, cutoff: date, dao) -> None:
        self.invoice_id = inv_id
        self.release_cutoff = cutoff
        self.dao = dao

    def is_invoice_released(self) -> bool:  # Get invoice's status from DAO
        status = self.dao.lookup_status(self.invoice_id)
        return status == 1 and self.release_cutoff >= date.today()


if __name__ == '__main__':
    inv_id: int = 0
    invoice = Invoice(inv_id, date(2021, 12, 31), InvoiceDataAccessObject())
    if invoice.is_invoice_released():
        print(f'invoice {inv_id} is released')
    print('Done')
