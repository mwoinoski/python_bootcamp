"""
Defines class for ETL processing
"""

from typing import Any


# TODO Step 1: define a class named EtlProcess
class EtlProcess:
    """ EtlProcess orchestrates the ETL process """

    # TODO Step 1: define an __init__ method that takes 3 arguments,
    #       the extractor, the transformer, and the loader
    def __init__(self, extractor, transformer, loader) -> None:
        """ Initialize the EtlProcess """

        # TODO Step 4: if any of the constructor arguments is not set,
        #      raise a ValueError
        if not extractor:
            raise ValueError('extractor is None')
        if not transformer:
            raise ValueError('transformer is None')
        if not loader:
            raise ValueError('loader is None')

        # TODO Step 1: save each of the constructor arguments in
        #      a data attribute in the EtlProcess object
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    # TODO Step 1: define a method named run that has 1 argument, self
    def run(self) -> None:
        """ Run the ETL process """
        # TODO Step 2: put the code inside a `try` statement
        try:
            # TODO Step 1: call the extractor's extract method and save the
            #      return value in a variable named `data`
            data = self.extractor.read_from_db()

            # TODO Step 1: call the transformer's transform method,
            #      passing `data` as the argument and saving the return value
            #      in a variable named `transformed_data`
            transformed_data = self.transformer.clean_data(data)

            # TODO: Step 1: call the loader's load method, passing
            #      `tranformed_data` as the argument
            self.loader.write_to_db(transformed_data)

        # TODO Step 2: define a handler for Exception
        except Exception as ex:
            print(f'Exception during ETL processing')
            # TODO Step 2: raise an EtlProcessError
            raise EtlProcessError from ex


# TODO Step 2: define an exception class EtlProcessError
# HINT: the class must extend the Exception class
#       the class body can consist of just the `pass` statement
class EtlProcessError(Exception):
    """ Exception class for ETL processing errors"""
    pass
