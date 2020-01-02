"""
Address class encapsulates information about a physical address.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    street1: str
    street2: Optional[str]
    city: str
    state_province: str
    postal_code: str
    country: str
