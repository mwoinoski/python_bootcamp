"""
Define the Address class
"""

import re
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Address:
    street1: str
    street2: str
    city: str
    state_province: str
    postal_code: str
    country: str = "US"
