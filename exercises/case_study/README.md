# Overview

``case_study`` is the case study project for the Sutter Python Bootcamp.

## Project Directory Structure

This is an example of the Python project directory structure recommended
by the Python Packaging Authority (PyPA). See pypa.org

- case_study: project root directory
  - case_study: source code directory; root of package hierachy
    - etl: top-level package for ETL classes
      - extract: package for Extracter classes
      - transform: package for Transformer classes
      - load: package for Loader classes
  - data: directory for data files (optional)
  - tests: unit tests
    - etl: tests for top-level ETL classes
      - extract: unit tests for Extracter classes
      - transform: unit tests for Transformer classes
      - load: unit test for Loader classes
  - .coveragerc: configuration settings for pytest code coverage plugin
  - config.ini: application configuration settings (optional)
  - logging.ini: logger configuration settings
  - MANIFEST.in: tells setup.py which files to include in the built distro
  - mypy.ini: mypy configuration file (optional)
  - README.md: overview of this project in MarkDown format
  - setup.cfg: configuration for setup.py script

### Basic transformations

