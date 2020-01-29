"""
Unit test for EtlProcess
"""

from unittest.mock import Mock

from pyspark.sql import SparkSession
from pytest import raises

from case_study.etl.etl_process import EtlProcess, EtlProcessError
from case_study.etl.extractor import ExtractorCsv
from case_study.etl.loader import LoaderCsv
from case_study.etl.transform.transformer import TransformerTopFiveCust


class TestEtlProcess:
    def test_run_success(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=ExtractorCsv)
        transformer = Mock(spec=TransformerTopFiveCust)
        loader = Mock(spec=LoaderCsv)
        etl_process = EtlProcess(extractor, transformer, loader, spark)

        etl_process.run()

        assert extractor.read_from_db.called
        assert transformer.clean_data.called
        assert loader.write_to_db.called
        assert spark.stop.called

    def test_run_extract_raises_exception(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=ExtractorCsv)
        extractor.read_from_db.side_effect = EtlProcessError()
        transformer = Mock(spec=TransformerTopFiveCust)
        loader = Mock(spec=LoaderCsv)

        etl_process = EtlProcess(extractor, transformer, loader, spark)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.read_from_db.called
        assert not transformer.clean_data.called
        assert not loader.write_to_db.called
        assert spark.stop.called

    def test_run_transform_raises_exception(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=ExtractorCsv)
        transformer = Mock(spec=TransformerTopFiveCust)
        transformer.clean_data.side_effect = EtlProcessError()
        loader = Mock(spec=LoaderCsv)

        etl_process = EtlProcess(extractor, transformer, loader, spark)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.read_from_db.called
        assert transformer.clean_data.called
        assert not loader.write_to_db.called
        assert spark.stop.called

    def test_run_load_raises_exception(self):
        spark = Mock(spec=SparkSession)
        extractor = Mock(spec=ExtractorCsv)
        transformer = Mock(spec=TransformerTopFiveCust)
        loader = Mock(spec=LoaderCsv)
        loader.write_to_db.side_effect = EtlProcessError()

        etl_process = EtlProcess(extractor, transformer, loader, spark)

        with raises(EtlProcessError):
            etl_process.run()

        assert extractor.read_from_db.called
        assert transformer.clean_data.called
        assert loader.write_to_db.called
        assert spark.stop.called
