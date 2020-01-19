"""
Base class for all facilities
"""

from facilities.address import Address


# TODO: define a class named Facility
class Facility:
    # TODO: define three data attribute named cert_number (an int), name (a string),
    #       and address (a string)
    cert_number: int
    name: str
    address: str

    # TODO: define the __init__ method
    #       __init__ should have 4 args: self, cert_number, name, address
    def __init__(self, cert_number: int, name: str, address: str):
        # TODO: assign cert_number, name and address to the data atttributes
        #       with the same names
        self.cert_number = cert_number
        self.name = name
        self.address = address

    # TODO: define the __str__ method
    #       __str__ should return the facility's name
    def __str__(self):
        return self.name
