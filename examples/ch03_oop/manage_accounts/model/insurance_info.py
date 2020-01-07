"""
Details of a Patient's insurance carrier.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class InsuranceInfo:
    database_id: Optional[str]
    provider_name: str
    plan_name: str
    account_id: str
    group_id: Optional[str]
    rx_bin_id: Optional[str]
