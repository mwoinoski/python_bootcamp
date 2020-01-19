"""
Define the Address class
"""


# TODO: define a class named Address
class Address:
    # TODO: define four string data attributes: street, city, state, zip
    street: str
    city: str
    state: str
    zip_code: str

    # TODO: define the __init__ method
    #       __init__ should have 5 args: self, street, city, state, zip
    def __init__(self, street: str, city: str, state: str, zip: str):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip

    # TODO: define the __str__ method
    #       __str__ should return a string formed by concatenating all Address attributes
    def __str__(self):
        return f'{self.street} {self.city} {self.state} {self.zip_code}'
