"""
Defines class for ETL processing
"""


# TODO Step 1: define a class named EtlProcess
class ....

    # TODO Step 1: define an __init__ method that takes 3 arguments,
    #       the extractor, the transformer, and the loader
    def ....

        # TODO Step 4: if any of the constructor arguments is not set,
        #      raise a ValueError


        # TODO Step 1: save each of the constructor arguments in
        #      a data attribute in the EtlProcess object
        ....

    # TODO Step 1: define a method named run that has 1 argument, self
    def ....
        # TODO Step 2: put the code inside a `try` statement
            # TODO Step 1: call the extractor's extract method and save the
            #      return value in a variable named `data`
            data = ....

            # TODO Step 1: call the transformer's transform method,
            #      passing `data` as the argument and saving the return value
            #      in a variable named `transformed_data`
            transformed_data = ....

            # TODO: Step 1: call the loader's load method, passing
            #      `tranformed_data` as the argument
            ....

        # TODO Step 2: define a handler for Exception

            # TODO Step 2: raise an EtlProcessError



# TODO Step 2: define an exception class EtlProcessError
# HINT: the class must extend the Exception class
#       the class body can consist of just the `pass` statement

