"""
Utility functions for handling person records in our application.
"""

# build full name from person's  family name, middle name, and given name
def get_full_name(given, middle, family):
    if middle is None and family is None:
        return given
    if middle is None:
        return given + ' ' + family
    return given + ' ' + middle + ' ' + str(family)
