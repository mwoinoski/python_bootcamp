"""
Provider class that defines the attributes of health care providers
"""

from datetime import datetime
from typing import Optional

from manage_accounts.model.person import Person


def is_valid_npi(npi):
    """
    return True if npi is a valid NPI, False otherwise

    NPI must be 10 digits long
    First digit must be a 1 or 2
    Last digit is check digit
    """
    return npi is not None and \
        npi.isdecimal() and \
        len(npi) == 10 and \
        npi[0] in "12" and \
        npi[9] == calc_check_digit(npi[:9])


def calc_check_digit(npi_first9):
    """
    Return the check digit for the given NPI.
    The check digit calculated by the Luhn algorithm; see
    https://www.cms.gov/Regulations-and-Guidance/Administrative-Simplification/NationalProvIdentStand/Downloads/NPIcheckdigit.pdf

    :return: True if npi is a valid NPI, False otherwise
    """
    total: int = 24  # adjustment for prefix for health app in the US (80840)
    for i in range(0, len(npi_first9)):
        if i % 2:
            total += int(npi_first9[i])
        else:
            doubled = int(npi_first9[i]) * 2
            total += doubled // 10 + doubled % 10
    next_multiple_of_10 = (total + 9) // 10 * 10
    check_digit = next_multiple_of_10 - total
    return str(check_digit)

    # Here's the Luhn algorithm, exactly as described in the cms.gov link:
    #   digits_at_even_indexes = [int(npi_first9[i])
    #                             for i in range(1, len(npi_first9), 2)]
    #   digits_at_odd_pos_doubled = [int(npi_first9[i]) * 2
    #                                for i in range(0, len(npi_first9), 2)]
    #   digits_at_odd_pos_summed = [n // 10 + n % 10
    #                              for n in digits_at_odd_pos_doubled]
    #   total: int = 24  # adjustment for prefix for health application in USA
    #   for n in digits_at_odd_pos_summed + digits_at_even_indexes:
    #       total += n
    #   return str((total + 9) // 10 * 10 - total)

    # And if you want to show off your Python tricks:
    # total: int = 24  # adjustment for prefix for health app in USA (80840)
    # for digit in [int(c) * (1 if i % 2 else 2) for c in npi_first9]:
    #     total += digit // 10 + digit % 10
    # return str((total + 9) // 10 * 10 - total)
