"""
Dummy DAO for invoice queries.
"""


class InvoiceDataAccessObject:
    def __init__(self) -> None:
        self.usage_count = 0
        # production version sets up connection to DB

    def lookup_status(self, invoice_id: int) -> int:
        if invoice_id < 1:
            raise ValueError(f'invalid invoice_id {invoice_id}')

        self.usage_count += 1
        return self.usage_count

    def set_released_status(self, invoice) -> bool:
        return True
