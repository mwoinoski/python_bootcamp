"""
Unit test for top-level EtlProcess class
"""

from unittest.mock import Mock
from pytest import raises

from etl_process import EtlProcess, EtlProcessError


class TestEtlProcess:
    # TODO Step 1: write a test case that tests the success path of
    #      an execution of the EtlProcess run() method
    def test_run_success(self):
        # TODO: create 3 mock objects for the extractor, transformer,
        #       and loader objects
        extractor = Mock()
        transformer = Mock()
        loader = Mock()

        # TODO: create an EtlProcess object, passing the 3 mock objects
        #       as parameters
        etl_process = EtlProcess(extractor, transformer, loader)

        # TODO: call the EtlProcess run() method
        etl_process.run()

        # TODO: verify that the extract() method of the mock extractor was called
        assert extractor.extract.called

        # TODO: verify that the transform() method of the mock transformer was called
        assert transformer.transform.called

        # TODO: verify that the loader() method of the mock loader was called
        assert loader.load.called

    # TODO Step 2: write a test case that tests an error path of
    #      an execution of the EtlProcess run() method
    def test_run_extract_raises_exception(self):
        # TODO: create 3 mock objects
        extractor = Mock()
        transformer = Mock()
        loader = Mock()

        # TODO: set the side effect of the mock extractor's extract() method
        #       to a RuntimeError
        extractor.extract.side_effect = RuntimeError()

        # TODO: create an EtlProcess
        etl_process = EtlProcess(extractor, transformer, loader)

        # TODO: use pytest's raises function to verify an EtlProcessError
        #       (note that the extractor raises a RuntimeError, but the
        #        EtlProcessor should raise an EtlProcessError)
        with raises(EtlProcessError):
            # TODO: call the EtlProcess's run method
            etl_process.run()

        # TODO: assert that the mock extractors extract method was called,
        #       but the transformer's transform method and the loader's load
        #       method were not called
        assert extractor.extract.called
        assert not transformer.transform.called
        assert not loader.load.called

    # TODO Step 3: test a different an error path

    # TODO: write a test case similar to the previous test case, except
    #       it verfies that
    def test_run_transform_raises_exception(self):
        extractor = Mock()
        transformer = Mock()
        loader = Mock()

        # TODO: set the side effect of the mock transformers's transform() method
        #       to a RuntimeError
        transformer.transform.side_effect = RuntimeError()

        etl_process = EtlProcess(extractor, transformer, loader)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.extract.called
        assert transformer.transform.called
        assert not loader.load.called

    # TODO Step 4: verify that EtlProcess raises exceptions if any argument
    #      to its constructor is None

    def test_init_validates_extractor(self):
        with raises(ValueError):
            EtlProcess(None, Mock(), Mock())

    def test_init_validates_transformer(self):
        with raises(ValueError):
            EtlProcess(Mock(), None, Mock())

    def test_init_validates_loader(self):
        with raises(ValueError):
            EtlProcess(Mock(), Mock(), None)
