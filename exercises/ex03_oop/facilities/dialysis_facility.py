"""
InPatientRehab class definition.
"""

from facilities.facility import Facility


# TODO: define DialysisFacility class as a subclass of Facility
class ....
    # TODO: define a data attribute named number_of_dialsis_machines (an int)


    # TODO: define the __init__ method
    #       __init__ should have 5 args: self, cert_number, name, address, and
    #       number of dialysis machines
    def ....
        # TODO: call the superclass __init__ method with arguments cert_number, name, address


        # TODO: save the number of dialysis machines in the number_of_dialysis_machines attribute


    # TODO: define the __str__ method
    # HINT: to call the superclass method, user super().__str__()
    def ....
        # TODO: return a string formed by concatenating the results
        #       of the superclass's __str__ method and the number_of_dialysis machines
        return ....

    # TODO: define calculate_quality_score method
    def ....
        # TODO: return 3 * (the number of dialysis machines)
        return ....


