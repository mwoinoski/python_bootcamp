"""
Defines the Patient class
"""

from copy import deepcopy
from typing import List, Optional

from person.person import Person
from person.insurance_info import InsuranceInfo


class Patient(Person):
    insuranceInfo: List[InsuranceInfo]

    def __init__(self, family: str, given: str, middle: str,
                 ins_info: Optional[List[InsuranceInfo]] = None) -> None:
        super().__init__(family, given, middle)
        self.insurance_info = list()
        if ins_info:
            for info in ins_info:
                self.add_ins_info(info)

    def add_ins_info(self, info: InsuranceInfo) -> None:
        self.insurance_info.append(deepcopy(info))

    def remove_ins_info(self, provider_name: str, account_id: str) \
            -> Optional[InsuranceInfo]:
        # you can't remove items from a list while you're iterating over it,
        # so use the list constructor to create a (shallow) copy
        for info in list(self.insurance_info):  # iterate over the copy
            if info.provider_name == provider_name and \
                    info.account_id == account_id:
                self.insurance_info.remove(info)  # remove item from original list
                return info
        return None

    def __eq__(self, other):
        """ Called when Patient instances are compared with == operator """
        return isinstance(other, Patient) and \
            super().__eq__(other) and \
            other.insurance_info == self.insurance_info
