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

    us_zip_code_re: ClassVar[str] = r'^\d{5}(-\d{4})?$'

    ca_postal_code_re: ClassVar[str] = \
        r'^(?!.*[DFIOQU])[A-VXY][0-9][A-Z] ?[0-9][A-Z][0-9]$'

    def __post_init__(self):
        if not Address.is_valid_postal_code(self.postal_code, self.country):
            msg = f'"{self.postal_code}" not a valid {self.country} postal code'
            raise ValueError(msg)

    @classmethod
    def is_valid_postal_code(cls, code: str, country: str = 'US'):
        return not country or \
            country == "US" and bool(re.match(cls.us_zip_code_re, code)) or\
            country == "CA" and bool(re.match(cls.ca_postal_code_re, code))
