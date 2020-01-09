"""
Demo of user-defined exceptions in chapter 4.
"""

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
        except DaoError as dao_error:
            print(f'DaoError: {dao_error}')
            return False


if __name__ == '__main__':
    dao = InvoiceDao('Invoices')
    try:
        # invoice = Invoice(-1, InvoiceDao())
        # print(f'invoice is {"" if invoice.is_invoice_released() else "un"}'
        #       f'released')
        status = dao.lookup_status(-1)  # forces an exception
        print(f'status is {status}')
    except DaoError as de:
        print(f'DaoError: {de}')
    except Exception as ex:
        print(f'Exception: {ex}')
    finally:
        dao.close()  # clean up

    print('Done with main')
