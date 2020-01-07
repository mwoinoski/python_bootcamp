"""
Base class for all facilities
"""

from abc import ABCMeta, abstractmethod

from facilities.address import Address


# TODO: define a class named Facility
class Facility(metaclass=ABCMeta):
    address: Address

    # TODO: define __init__ method
    # HINT: args...
    def __init__(self):
        pass

    # TODO: define abstract method
    @abstractmethod
    def calculate_quality_score(self):
        pass
