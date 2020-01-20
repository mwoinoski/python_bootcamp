"""
Simple Person class for demos
"""

from dataclasses import dataclass


@dataclass
class Provider:
    """ Simple entity class for testing mock objects """
    provider_id: int
    first_name: str
    middle_name: str
    last_name: str
