"""
Unit test for top-level EtlProcess class
"""

from unittest.mock import Mock
from pytest import raises

from etl_process import EtlProcess, EtlProcessError


class TestEtlProcess:
    # TODO Step 1: write a test case that tests the success path of
    #      an execution of the EtlProcess run() method
    def ....
        # TODO: create 3 mock objects for the extractor, transformer,
        #       and loader objects
        ....

        # TODO: create an EtlProcess object, passing the 3 mock objects
        #       as parameters
        etl_process = ....

        # TODO: call the EtlProcess run() method
        ....

        # TODO: verify that the extract() method of the mock extractor was called
        assert ....

        # TODO: verify that the transform() method of the mock transformer was called
        ....

        # TODO: verify that the load() method of the mock loader was called
        ....

#     # TODO Step 2: write a test case that tests an error path of
#     #      an execution of the EtlProcess run() method
#     def test_run_extract_raises_exception(self):
#         # TODO: create 3 mock objects
#         ....
#
#         # TODO: set the side effect of the mock extractor's extract() method
#         #       to a RuntimeError
#         ....
#
#         # TODO: create an EtlProcess
#         ....
#
#         # TODO: use pytest's raises function to verify an EtlProcessError
#         #       (note that the extractor raises a RuntimeError, but the
#         #        EtlProcessor should raise an EtlProcessError)
#         with ....
#             # TODO: call the EtlProcess's run method
#             ....
#
#         # TODO: assert that the mock extractors extract method was called,
#         #       but the transformer's transform method and the loader's load
#         #       method were not called
#         ....
#
#     # TODO Step 3: test a different an error path
#
#     # TODO: write a test case similar to the previous test case, except
#     #       it verfies that
#     def test_run_transform_raises_exception(self):
#         # TODO: create 3 mocks and an EtlProcess
#         ....
#
#         # TODO: set the side effect of the mock transformers's transform() method
#         #       to a RuntimeError
#         ....
#
#         # TODO: use pytest's raises function to verify an EtlProcessError
#         ....
#             # TODO: call the EtlProcess's run method
#             ....
#
#         # TODO: assert that the mock extractor's extract method and the
#         #       mock transformer's transform method were called, but
# #       #       the mock loader's load method was not called not called
#         ....
#
#
#     # TODO Step 4: write 3 test methods to verify that EtlProcess raises
#     #      EtlProcess exceptions if any argument to its constructor is None
#
#     ....
