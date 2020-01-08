"""
Invoice class example from chapter 5.
"""

from datetime import date


class Invoice:
    invoice_id: int
    release_cutoff: date  # from datetime

    def __init__(self, inv_id: int, cutoff: date, dao) -> None:
        self.invoice_id = inv_id
        self.release_cutoff = cutoff
        self.data_access = dao

    def is_invoice_released(self) -> bool:  # Get invoice's status from DAO
        try:
            status = self.data_access.lookup_status(self.invoice_id)
            return status == 1 and self.release_cutoff >= date.today()
        except ValueError:
            return False

    # def is_invoice_released(self) -> bool:  # Get invoice's status from DAO
    #     status = self.data_access.lookup_status(self.invoice_id)
    #     return status == 1 and self.release_cutoff >= date.today()
