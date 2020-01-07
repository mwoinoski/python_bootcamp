"""
Define the Address class
"""
from dataclasses import dataclass


@dataclass
class Address:
    street1: str
    street2: str
    city: str
    state_province: str
    postal_code: str
