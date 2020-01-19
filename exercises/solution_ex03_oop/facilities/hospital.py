"""
Hospital class definition.
"""

from facilities.facility import Facility


# TODO: define Hospital class as a subclass of Facility
class Hospital(Facility):
    # TODO: define an attribute named number_of_beds with type int
    number_of_beds: int

    # TODO: define the __init__ method
    #       __init__ should have 5 args: self, cert_number, name, address, and number of beds
    def __init__(self, cert_number: int, name: str, address: str, beds: int):
        # TODO: call the superclass __init__ method with arguments cert_number, name, address
        super().__init__(cert_number, name, address)
        # TODO: save the number of beds in the number_of_beds attribute
        self.number_of_beds = beds

    # TODO: define the __str__ method
    #       __str__ should return a string formed by concatenating the results
    #       of the superclass's __str__ method and the number of beds
    def __str__(self):
        return super().__str__() + \
            f': {self.number_of_beds} beds'

    # TODO: define calculate_quality_score method
    #       for now, calculate_quality_score should return the number of beds times 2
    def calculate_quality_score(self):
        print('Hospital.calculate_quality_score was called')
        return self.number_of_beds * 2
