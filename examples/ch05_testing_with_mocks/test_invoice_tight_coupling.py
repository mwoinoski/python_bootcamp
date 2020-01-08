"""
Test of @patch
"""

# pylint: disable=missing-class-docstring,missing-function-docstring,no-self-use

from unittest.mock import Mock, patch

from datetime import date

from invoice_tight_coupling import Invoice


class TestInvoiceTest:
    def test_is_invoice_released_status_1_today_no_patch(self):

        mock_dao = Mock()
        mock_dao.lookup_status.return_value = 1

        invoice = Invoice(1234, date.today())
        invoice.dao = mock_dao  # replace production DAO

        assert invoice.is_invoice_released()

    @patch('invoice_tight_coupling.InvoiceDataAccessObject')
    def test_is_invoice_released_status_1_today_with_patch(self, mock_class):

        mock_dao = mock_class()

        mock_dao.lookup_status.return_value = 1

        invoice = Invoice(1234, date.today())

        assert invoice.is_invoice_released()

    def test_is_invoice_released_status_0_today_no_patch(self):

        mock_dao = Mock()
        mock_dao.lookup_status.return_value = 0

        invoice = Invoice(1234, date.today())
        invoice.dao = mock_dao  # replace production DAO

        assert not invoice.is_invoice_released()

    @patch('invoice_tight_coupling.InvoiceDataAccessObject')
    def test_is_invoice_released_status_0_today_with_patch(self, mock_class):

        mock_dao = mock_class()

        mock_dao.lookup_status.return_value = 0

        invoice = Invoice(1234, date.today())

        assert not invoice.is_invoice_released()
