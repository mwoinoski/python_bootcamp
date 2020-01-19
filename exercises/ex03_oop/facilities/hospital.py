"""
Hospital class definition.
"""

from facilities.facility import Facility


# TODO: define Hospital class as a subclass of Facility
class ....
    # TODO: define an attribute named number_of_beds with type int


    # TODO: define the __init__ method
    #       __init__ should have 5 args: self, cert_number, name, address, and number of beds
    def ....
        # TODO: call the superclass __init__ method with arguments cert_number, name, address
        ....
        # TODO: save the number of beds in the number_of_beds attribute
        ......

    # TODO: define the __str__ method
    def __str__(self):
        # TODO: __str__ should return a string formed by concatenating the results
        #       of the superclass's __str__ method and the number of beds
        return ....

    # TODO: define calculate_quality_score method
    def ....
        # TODO: return 2 * (the number of beds)
        return ....
