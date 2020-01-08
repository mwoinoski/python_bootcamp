"""
Invoice class example from chapter 5.
In this example, Invoice is tightly coupled to InvoiceDataAccessObject.
"""

from datetime import date

from invoice_data_access_object import InvoiceDataAccessObject


class Invoice:
    invoice_id: int
    release_cutoff: date  # from datetime
    dao: InvoiceDataAccessObject

    def __init__(self, inv_id: int, cutoff: date) -> None:
        self.invoice_id = inv_id
        self.release_cutoff = cutoff
        self.dao = InvoiceDataAccessObject()  # classes are tightly coupled

    def is_invoice_released(self) -> bool:  # Get invoice's status from DAO
        status = self.dao.lookup_status(self.invoice_id)
        return status == 1 and self.release_cutoff >= date.today()


if __name__ == '__main__':
    invoice = Invoice(1234, date(2021, 12, 31))

    print(f'is_invoice_released? {invoice.is_invoice_released()}')
