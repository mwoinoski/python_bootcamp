"""
Unit test for EtlProcess
"""

from unittest.mock import Mock

from pyspark.sql import SparkSession
from pytest import raises

from etl_process import EtlProcess, EtlProcessError
from extractor import Extractor
from loader import Loader
from transformer import Transformer


class TestEtlProcess:
    def test_run_success(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=Extractor)
        transformer = Mock(spec=Transformer)
        loader = Mock(spec=Loader)
        etl_process = EtlProcess(spark, extractor, transformer, loader)

        etl_process.run()

        assert extractor.extract.called
        assert transformer.transform.called
        assert loader.load.called
        assert spark.stop.called

    def test_run_extract_raises_exception(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=Extractor)
        extractor.extract.side_effect = EtlProcessError()
        transformer = Mock(spec=Transformer)
        loader = Mock(spec=Loader)

        etl_process = EtlProcess(spark, extractor, transformer, loader)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.extract.called
        assert not transformer.transform.called
        assert not loader.load.called
        assert spark.stop.called

    def test_run_transform_raises_exception(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=Extractor)
        transformer = Mock(spec=Transformer)
        transformer.transform.side_effect = EtlProcessError()
        loader = Mock(spec=Loader)

        etl_process = EtlProcess(spark, extractor, transformer, loader)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.extract.called
        assert transformer.transform.called
        assert not loader.load.called
        assert spark.stop.called

    def test_run_load_raises_exception(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=Extractor)
        transformer = Mock(spec=Transformer)
        loader = Mock(spec=Loader)
        loader.load.side_effect = EtlProcessError()

        etl_process = EtlProcess(spark, extractor, transformer, loader)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.extract.called
        assert transformer.transform.called
        assert loader.load.called
        assert spark.stop.called
