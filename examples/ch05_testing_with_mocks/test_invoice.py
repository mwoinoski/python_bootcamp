"""
Unit tests for Invoice.

The dependency on the InvoiceDataAccessObject DAO will be mocked.
"""

# pylint: disable=missing-class-docstring,missing-function-docstring,no-self-use

from unittest.mock import Mock
from datetime import date, timedelta
from pytest import mark

from invoice import Invoice
from invoice_data_access_object import InvoiceDataAccessObject


class TestInvoiceTest:
    def test_is_invoice_released_status_1_tomorrow(self) -> None:
        cutoff = date.today() + timedelta(days=1)

        mock_dao = Mock(spec=InvoiceDataAccessObject)
        mock_dao.lookup_status.return_value = 1

        invoice = Invoice(1234, cutoff, mock_dao)

        assert invoice.is_invoice_released()

    def test_is_invoice_released_dao_raises_value_error(self) -> None:
        mock_dao = Mock(spec=InvoiceDataAccessObject)
        mock_dao.lookup_status.side_effect = ValueError('No invoice with ID 1234')

        invoice = Invoice(1234, date.today(), mock_dao)

        assert not invoice.is_invoice_released()

    def test_is_invoice_released_status_1_today(self) -> None:
        cutoff = date.today() + timedelta(days=0)

        mock_dao = Mock(spec=InvoiceDataAccessObject)
        mock_dao.lookup_status.return_value = 1

        invoice = Invoice(1234, cutoff, mock_dao)

        assert invoice.is_invoice_released()

    def test_is_invoice_released_status_1_yesterday(self) -> None:
        cutoff = date.today() + timedelta(days=-1)

        mock_dao = Mock(spec=InvoiceDataAccessObject)
        mock_dao.lookup_status.return_value = 1

        invoice = Invoice(1234, cutoff, mock_dao)

        assert not invoice.is_invoice_released()

    def test_is_invoice_released_status_0_tomorrow(self) -> None:
        cutoff = date.today() + timedelta(days=1)

        mock_dao = Mock(spec=InvoiceDataAccessObject)
        mock_dao.lookup_status.return_value = 0

        invoice = Invoice(1234, cutoff, mock_dao)

        assert not invoice.is_invoice_released()

    def test_is_invoice_released_status_0_today(self) -> None:
        cutoff = date.today() + timedelta(days=0)

        mock_dao = Mock(spec=InvoiceDataAccessObject)
        mock_dao.lookup_status.return_value = 0

        invoice = Invoice(1234, cutoff, mock_dao)

        assert not invoice.is_invoice_released()

    def test_is_invoice_released_status_0_yesterday(self) -> None:
        cutoff = date.today() + timedelta(days=-1)

        mock_dao = Mock(spec=InvoiceDataAccessObject)
        mock_dao.lookup_status.return_value = 0

        invoice = Invoice(1234, cutoff, mock_dao)

        assert not invoice.is_invoice_released()

    # parameterized test: tests all 6 conditions with one method
    @mark.parametrize('status, time_delta, expected', [
        (1, 1, True),
        (1, 0, True),
        (1, -1, False),
        (0, 1, False),
        (0, 0, False),
        (0, -1, False),
    ])
    def test_is_invoice_released(self, status: int, time_delta: int,
                                 expected: bool) -> None:
        cutoff = date.today() + timedelta(days=time_delta)

        mock_dao = Mock(spec=InvoiceDataAccessObject)
        mock_dao.lookup_status.return_value = status

        invoice = Invoice(1234, cutoff, mock_dao)

        assert invoice.is_invoice_released() == expected
