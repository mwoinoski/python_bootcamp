"""
Defines the Patient class
"""
from copy import deepcopy
from datetime import datetime
from typing import List, Optional

from manage_accounts.model.person import Person
from manage_accounts.model.insurance_info import InsuranceInfo


class Patient(Person):
    _insurance_info: List[InsuranceInfo]

    def __init__(self,
                 given: Optional[str] = None,
                 middle: Optional[str] = None,
                 family: Optional[str] = None,
                 patient_id: Optional[str] = None,
                 timestamp: Optional[datetime] = None
                 ) -> None:
        super().__init__(given, middle, family, patient_id, timestamp)
        self._insurance_info = list()

    def add_ins_info(self, info: InsuranceInfo) -> None:
        self._insurance_info.append(info)

    def remove_ins_info(self, database_id: str) -> Optional[InsuranceInfo]:
        # you can't remove items from a list while you're iterating over it,
        # so use the list constructor to create a copy
        for info in list(self._insurance_info):  # iterate over the copy
            if info.database_id == database_id:
                self._insurance_info.remove(info)  # remove item from original list
                return info
        return None

    @property
    def insurance_info(self):
        """
        This is the getter for the insurance info list. We return a copy of
        the list so the caller can't accidently change the internal state of
        the Patient.
        """
        return deepcopy(self._insurance_info)
