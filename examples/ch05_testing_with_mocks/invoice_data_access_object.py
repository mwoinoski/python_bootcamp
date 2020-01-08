"""
Data Access Object (DAO) for invoice processing.
"""


class InvoiceDataAccessObject:
    def __init__(self) -> None:  # set up connection to DB
        print('Production InvoiceDataAccessObject constructor called')

    def lookup_status(self, invoice_id: int) -> int:
        status: int = 0
        print(f'\nProduction InvoiceDataAccessObject lookup_status({invoice_id}) '
              f'called, returning {status}')
        return 0
