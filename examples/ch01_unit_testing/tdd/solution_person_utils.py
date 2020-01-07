"""
Utility functions for handling person records in our application.
"""

# TODO: define function to build full name from person's given name, middle name, and family name


def get_full_name(family_name, given_name, middle_name):
    """ Concatenate all name attributes with no additional spaces """
    names = [given_name, middle_name, family_name]
    return " ".join(n for n in names if n)


# TODO: define function to split an address string into city, state/province, and zip code
