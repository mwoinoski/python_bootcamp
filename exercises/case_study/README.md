# Overview

``case_study`` is the case study project for the Sutter Python Bootcamp.

## ETL

### Basic transformations

* Cleaning
  - Mapping NULL to 0
  - Mapping 'No Value' to NULL
  - Mapping "Male" to "M" and "Female" to "F"
  - Date format consistency
  - Checking person age rangs (0-130)
  - Convert 2-digit year to 4-digit year
    DOB 01/02/18 - 2018 or 1918? pediatric facility: 2018, nursing home: 1918
* Deduplication
  - Identifying and removing duplicate records
* Format revision
  - Character set conversion
  - Unit of measurement conversion
  - Date/time conversion
* Key restructuring
  - Establishing key relationships across tables
* Change data types, e.g. DATETIME to TIMESTAMP
* Add values, e.g., timestamp, created_by, updated_by

### Advanced transformations

* Derivation: Applying business rules to your data that derive new calculated values 
  from existing data
  - Ex: creating a revenue metric that subtracts taxes
* Filtering: Selecting only certain rows and/or columns
* Joining: Linking data from multiple sources
  - Ex: adding ad spend data across multiple platforms, such as Google Adwords 
    and Facebook Ads
* Splitting: Splitting a single column into multiple columns
  - Full name into family, given, middle
  - Address into street, city, state/province, country
* Data validation: Simple or complex data validation
  - Ex: if the first three columns in a row are empty then reject the row from processing
* Summarization: Values are summarized to obtain total figures which are calculated and stored
  at multiple levels as business metrics
  - Ex: adding up all purchases a customer has made to build a customer lifetime value (CLV) metric
* Aggregation: Data elements are aggregated from multiple data sources and databases
* Integration
  - Give each unique data element one standard name with one standard definition.
    Data integration reconciles different data names and values for the same data element.
  - Join unstructured data or streaming data with structured data

## TODO
* load from CSV files from HDFS and SS tables
