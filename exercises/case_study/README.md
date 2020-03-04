# Overview

``case_study`` is the case study project for the Sutter Python Bootcamp.

## Project Directory Structure

This is an example of the Python project directory structure recommended
by the Python Packaging Authority (PyPA). See ``pypa.org``.

* case_study - project root directory
  * case_study - source code directory; root of package hierachy
    * etl - top-level package for ETL classes
      * extract - package for Extracter classes
      * transform - package for Transformer classes
      * load - package for Loader classes
  * data - directory for data files (optional)
  * tests - unit tests
    * case_study - top-level tests directory
      * etl - tests for top-level ETL classes
        * extract - unit tests for Extracter classes
        * transform - unit tests for Transformer classes
        * load - unit test for Loader classes
  * .coveragerc - configuration settings for pytest code coverage plugin
  * config.ini - application configuration settings (optional)
  * logging.ini - logger configuration settings
  * MANIFEST.in - tells setup.py which files to include in the built distro
  * mypy.ini - mypy configuration file (optional)
  * README.md - overview of this project in MarkDown format
  * setup.cfg - configuration for setup.py script

## ETL Components

Note the ETL classes under ``case_study.etl.extract`` and related packages.
The extractors for CSV files and database tables have the same interface,
and can be combined with different transformers and extractors. See 
``case_study/etl/etl_driver.py`` for an example of usage.

## Unit tests for ETL components 

See ``tests/case_study/etl/load/test_loader_csv.py`` for examples of
using PySpark DataFrames for validating ETL results. In this case, the 
extract and load operations use CSV files, but the same technique 
can be used for operations on database tables. 

Because Pytest is not integrated with Spark, the DataFrames created
in the unit tests are not distributed on a cluster, so the size of the
DataFrames is limited. This in-memory DataFrame technique will still work
for farily large datasets (possibly up to a few million rows). However, 
for very large datasets, you'll need to write your test scripts and 
launch them with ``spark-submit``.

## Running Unit Tests 

```
cd python_bootcamp/exercises/case_study
python -m pytest -W ignore::DeprecationWarning tests
```

## Running the Driver

```
cd python_bootcamp/exercises/case_study
spark-submit case_study/etl/etl_driver.py
```

## Building the Project

```
pip install --user wheel
cd python_bootcamp/exercises/case_study
python setup.py clean
python setup.py build sdist bdist_wheel 
```

After building the project, you can install it in the current 
Python config using ``pip`` as usual. The best practice is to test the 
installation in a virtual environment before installing in a 
production Python:

```
/usr/bin/python3 -m venv testvenv
source testvenv/bin/activate
pip install dist/*.whl
```

After verifying the installation, you can simply delete the ``testvenv`` directory.

## TODO

* Define abstract base classes ``Extractor``, ``Loader``, and ``Transformer``. 
  Move duplicate code from ``ExtractorCsv`` and ``ExtractorDb``, etc., 
  to the appropriate base class.
* Define test cases for database operations. 
