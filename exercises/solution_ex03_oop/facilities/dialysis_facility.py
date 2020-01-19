"""
InPatientRehab class definition.
"""

from facilities.facility import Facility


# TODO: define DialysisFacility class as a subclass of Facility
class DialysisFacility(Facility):
    # TODO: define a data attribute named number_of_dialsis_machines (an int)
    number_of_dialysis_machines: int

    # TODO: define the __init__ method
    #       __init__ should have 5 args: self, cert_number, name, address, and
    #       number of dialysis machines
    def __init__(self, cert_number: int, name: str, address: str, num_of_machines: int):
        # TODO: call the superclass __init__ method with arguments cert_number, name, address
        super().__init__(cert_number, name, address)
        # TODO: save the number of dialysis machines in the number_of_dialysis_machines attribute
        self.number_of_dialysis_machines = num_of_machines

    # TODO: define the __str__ method
    #       __str__ should return a string formed by concatenating the results
    #       of the superclass's __str__ method and the number_of_dialysis machines
    # HINT: to call the superclass method, user super().__str__()
    def __str__(self):
        return super().__str__() + \
            f': {self.number_of_dialysis_machines} dialysis machines'

    # TODO: define calculate_quality_score method
    #       for now, calculate_quality_score should return the number of
    #       dialysis machines times 2
    def calculate_quality_score(self):
        print('DialysisFacility.calculate_quality_score was called')
        return self.number_of_dialysis_machines * 3


