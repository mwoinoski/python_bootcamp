"""
Defines the Patient class
"""
from datetime import datetime
from typing import List, Optional

from manage_accounts.model.person import Person
from manage_accounts.model.insurance_info import InsuranceInfo


class Provider(Person):
    npi: str

    def __init__(self,
                 npi: str,
                 given: Optional[str] = None,
                 middle: Optional[str] = None,
                 family: Optional[str] = None,
                 provider_id: Optional[str] = None,
                 timestamp: Optional[datetime] = None
                 ) -> None:
        super().__init__(given, middle, family, provider_id, timestamp)
        self.npi = npi

    def __repr__(self):
        return f"npi='{self.npi}'," + super().__repr__()

    def __str__(self):
        return repr(self)
