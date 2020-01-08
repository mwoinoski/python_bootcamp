"""
Base class for all facilities
"""

from facilities.address import Address


# TODO: define a class named Facility
class Facility:
    address: Address

    # TODO: define __init__ method
    # HINT: args...
    def __init__(self):
        pass

    # TODO: define abstract method
    def calculate_quality_score(self):
        pass
