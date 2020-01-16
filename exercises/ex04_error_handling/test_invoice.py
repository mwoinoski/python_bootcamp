"""
Test error handling in the invoice handling code.
"""
from dataclasses import dataclass

from pytest import raises
from datetime import datetime, timedelta

from invoice import Invoice, InvoiceDataAccessObject


@dataclass
class InvoiceDaoStub:
    status: int = 0
    exception: Exception = None

    def lookup_status(self, invoice_id: int) -> int:
        if self.exception:
            raise self.exception
        return self.status


class TestInvoiceHandler:
    nextweek: datetime = datetime.now() + timedelta(weeks=1)

    def test_is_invoice_release_status_1(self):
        dao = InvoiceDaoStub(1)
        invoice = Invoice(1, self.nextweek, dao)

        is_released = invoice.is_invoice_released()

        assert is_released

    def test_is_invoice_release_status_0(self):
        dao = InvoiceDaoStub(0)
        invoice = Invoice(1, self.nextweek, dao)

        is_released = invoice.is_invoice_released()

        assert is_released

    def test_is_invoice_release_dao_raises_value_error(self):
        dao = InvoiceDaoStub(ValueError('invoice invoice id -1'))
        invoice = Invoice(1, self.nextweek, dao)

        is_released = invoice.is_invoice_released()

        assert not is_released

    def test_is_invoice_release_dao_raises_runtime_error(self):
        dao = InvoiceDaoStub(RuntimeError('something bad happened'))
        invoice = Invoice(1, self.nextweek, dao)

        is_released = invoice.is_invoice_released()

        assert not is_released
