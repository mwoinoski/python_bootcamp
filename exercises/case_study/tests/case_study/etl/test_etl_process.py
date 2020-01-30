"""
Unit test for EtlProcess class
"""

from unittest.mock import Mock

from pyspark.sql import SparkSession
from pytest import raises

from case_study.etl.etl_process import EtlProcess, EtlProcessError
from case_study.etl.extract.extractor_csv import ExtractorCsv
from case_study.etl.load.loader_csv import LoaderCsv
from case_study.etl.transform.transformer_clean_qip_data import TransformerCleanQipData


class TestEtlProcess:
    def test_run_success(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=ExtractorCsv)
        transformer = Mock(spec=TransformerCleanQipData)
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
        transformer = Mock(spec=TransformerCleanQipData)
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
        transformer = Mock(spec=TransformerCleanQipData)
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
        transformer = Mock(spec=TransformerCleanQipData)
        loader = Mock(spec=LoaderCsv)
        loader.load.side_effect = EtlProcessError()

        etl_process = EtlProcess(extractor, transformer, loader, spark)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.extract.called
        assert transformer.transform.called
        assert loader.load.called
        assert spark.stop.called
