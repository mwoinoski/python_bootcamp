"""
Base class for all people
"""


class Person:
    def __init__(self, given: str, middle: str, family: str):
        self.given = given
        self.middle = middle
        self.family = family
