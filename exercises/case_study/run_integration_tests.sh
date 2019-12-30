#!/usr/bin/env bash
# Run ETL process and test the results

export PYTHONPATH=..

cd "$HOME/python_bootcamp/exercises/case_study"
spark-submit case_study/etl_demo.py
cd tests
pytest test_etl_process.py
