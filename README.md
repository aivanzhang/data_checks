# data_checks 
![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.7-blue.svg) 

**Create, schedule, and deploy data quality checks.**

## Overview
Exisiting data observability solutions are painfully static. data_checks provides a dynamic data observability framework that allows you to reuse existing Python code and/or write new Python code to define data quality checks. Inspired by Python's [unittest](https://docs.python.org/3/library/unittest.html), data_checks allows you to write data quality checks as easily and seamlessly as you would write unittests on your code.

Some reason you might use this library:
- Reuse existing Python code
- Greater control over how check definition and execution
- Infinitely extendible and customizable for any data quality use case
- Connect any database to store data related to checks and executions
- Async execution
- CRON scheduling
- Silencing
- Alerting to a specified endpoint
- Storage of all logs

Some additional features that are in the works (in order of priority):
1) Custom pre-built analytics and visualizations
2) More flexibility in specifying the parallelization options (see [Warning on Async Executions](#warning-on-async-executions))
3) Define before, after, on success and on failure actions based on data checks
4) Automatically generate data checks from the command line (as you would generate a database migration) and Jupyter Notebooks

## Define Settings
Before you can use the package, you need to first set up your settings. Create a settings file (e.g. `check_settings.py`) and define the following variables:
```python
# URL to the database where check and execution data will be stored
CHECKS_DATABASE_URL = None
# Module where checks are defined
CHECKS_MODULE = None
# Module where suites are defined
SUITES_MODULE = None
# Endpoint URL where alerts will be sent
ALERTING_ENDPOINT = None
# Default CRON schedule for suites
DEFAULT_SCHEDULE = None
```
Then, set the `CHECK_SETTINGS_MODULE` environment variable to the path to your settings file (e.g. `data_checks.check_settings`):
```bash
export CHECK_SETTINGS_MODULE=data_checks.check_settings
```
or in Python:
```python
os.environ["CHECK_SETTINGS_MODULE"] = "data_checks.check_settings"
```
Now you're ready to start defining checks and suites!
## Create Checks
The library exposes the `DataCheck` class (defined in `data_checks.data_check`) which you can use to write your checks. The `DataCheck` class is a simplified beginner friendly subclass of the base `Check` class (`data_checks.base.check`). The user can also directly subclass the `Check` class to create more advanced checks (see [(Advanced) Create Checks](#%28advanced%29-create-checks)).

## (Advanced) Create Checks
## (Advanced) Create Suites

## (Advanced) Create Group Data Suites

## Command Line Interface
After defining your suites and/or checks, you can run them as well as other actions from the command line.

### Run Checks

### Silencing Checks' Rules

### Run Suites


## Warning on Fully Async Executions

## References

### Hierarchy
### Execution Flow