"""
Unit test for EtlProcess
"""

from unittest.mock import Mock

from pyspark.sql import SparkSession
from pytest import raises

from etl_process import EtlProcess, EtlProcessError
from extractor import ExtractorCsv
from loader import LoaderCsv
from transformer import TransformerTopFiveCust


class TestEtlProcess:
    def test_run_success(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=ExtractorCsv)
        transformer = Mock(spec=TransformerTopFiveCust)
        loader = Mock(spec=LoaderCsv)
        etl_process = EtlProcess(extractor, transformer, loader, spark)

        etl_process.run()

        assert extractor.extract.called
        assert transformer.transform.called
        assert loader.load.called
        assert spark.stop.called

    def test_run_extract_raises_exception(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=ExtractorCsv)
        extractor.extract.side_effect = EtlProcessError()
        transformer = Mock(spec=TransformerTopFiveCust)
        loader = Mock(spec=LoaderCsv)

        etl_process = EtlProcess(extractor, transformer, loader, spark)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.extract.called
        assert not transformer.transform.called
        assert not loader.load.called
        assert spark.stop.called

    def test_run_transform_raises_exception(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=ExtractorCsv)
        transformer = Mock(spec=TransformerTopFiveCust)
        transformer.transform.side_effect = EtlProcessError()
        loader = Mock(spec=LoaderCsv)

        etl_process = EtlProcess(extractor, transformer, loader, spark)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.extract.called
        assert transformer.transform.called
        assert not loader.load.called
        assert spark.stop.called

    def test_run_load_raises_exception(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=ExtractorCsv)
        transformer = Mock(spec=TransformerTopFiveCust)
        loader = Mock(spec=LoaderCsv)
        loader.load.side_effect = EtlProcessError()

        etl_process = EtlProcess(extractor, transformer, loader, spark)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.extract.called
        assert transformer.transform.called
        assert loader.load.called
        assert spark.stop.called
