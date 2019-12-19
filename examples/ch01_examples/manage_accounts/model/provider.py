"""
Defines the Patient class
"""
from datetime import datetime
from typing import Optional

from manage_accounts.model.person import Person


# MW first, define provider_test.py
# MW define Provider with field npi:str
# MW then add test to ensure npi can't be modified by client code
# MW change npi to property
class Provider(Person):
    _npi: str

    def __init__(self,
                 npi: str,
                 given: Optional[str] = None,
                 middle: Optional[str] = None,
                 family: Optional[str] = None,
                 provider_id: Optional[int] = None,
                 timestamp: Optional[datetime] = None
                 ) -> None:
        if not self.is_valid_npi(npi):
            raise ValueError(f"NPI {npi} is not valid")

        super().__init__(given, middle, family, provider_id, timestamp)
        self._npi = npi

    @property
    def npi(self) -> str:
        return self._npi

    def __repr__(self):
        return f"npi='{self.npi}'," + super().__repr__()

    def __str__(self):
        return repr(self)

    @staticmethod
    def is_valid_npi(npi: str) -> bool:
        """
        NPI must be 10 digits long
        First digit must be a 1 or 2
        Last digit is check digit calculated by the Luhn algorithm; see
        https://www.cms.gov/Regulations-and-Guidance/Administrative-Simplification/NationalProvIdentStand/Downloads/NPIcheckdigit.pdf

        :return: True if npi is a valid NPI, False otherwise
        """
        return npi is not None and \
            npi.isdecimal() and \
            len(npi) == 10 and \
            npi[0] in "12" and \
            npi[9] == Provider.calc_check_digit(npi[:9])
        # MW add test with separate "if". After they pass, refactor to combine
        # MW conditions into a single complex condition.
        # if not npi:
        #     return False
        # if len(npi) != 10:
        #     return False
        # if not (npi[0] == "1" or npi[0] == "2"):
        #     return False
        # if npi[9] != Provider.calc_check_digit(npi[:9]):
        #     return False
        # return True

    @staticmethod
    def calc_check_digit(npi: str) -> str:
        total: int = 24  # adjust for prefix for health application in USA (80840)
        for i in range(0, len(npi)):
            if i % 2:
                total += int(npi[i])
            else:
                doubled = int(npi[i]) * 2
                total += doubled // 10 + doubled % 10
        next_multiple_of_10 = (total + 9) // 10 * 10
        check_digit = next_multiple_of_10 - total
        return str(check_digit)

        # digits_at_even_indexes = [int(npi[i]) for i in range(1, len(npi), 2)]
        # digits_at_odd_pos_doubled = [int(npi[i]) * 2 for i in range(0, len(npi), 2)]
        # digits_at_odd_pos_summed = [n // 10 + n % 10 for n in digits_at_odd_pos_doubled]
        # total: int = 24  # adjust for prefix for health application in USA
        # for n in digits_at_odd_pos_summed + digits_at_even_indexes:
        #     total += n
        # return str((total + 9) // 10 * 10 - total)

        # total: int = 24  # adjust for prefix for health app in USA (80840)
        # for digit in [int(npi[i]) * (1 if i % 2 else 2)
        #               for i in range(0, len(npi))]:
        #     total += digit // 10 + digit % 10
        # return str((total + 9) // 10 * 10 - total)
